#!/usr/bin/python
import sys
import csv
import datetime

  
# COMPSCI 383 Homework 0 
#  
# Fill in the bodies of the missing functions as specified by the comments and docstrings.


# Exercise 0. (8 points)
#  
def read_data(file_name):
    """Read in the csv file and return a list of tuples representing the data.

    Transform each field as follows:
      date: datetime.date
      mileage: integer
      location: string
      gallons: float
      price: float (you'll need to get rid of the '$')

    Do not return a tuple for the header row.  While you can process the raw text using string
    functions, to receive full credit you must use Python's built in csv module.

    If the field is blank, you should put a None value in the tuple for that field (for the 
    other functions below, you'll need to check for None values when making calculations).  

    Hint: to parse the date field, use the strptime function in the datetime module, and then
    use datetime.date() to create a date object.

    See: 
      https://docs.python.org/3/library/csv.html
      https://docs.python.org/3/library/datetime.html

    """
    rows = []  # this list should contain one tuple per row
    #
    # fill in function body here
    #
    with open(file_name) as csvfile:				#Opens inputted csv, skips the first header line, and converts the data into a list
    	readf = csv.reader(csvfile,delimiter=',')
    	next(readf)
    	data = list(readf)

    for r in data:
    	if r[0] != '':												# converts the date to a datetime object which is then converted to a date object, set to None if blank
    		r[0] = datetime.datetime.strptime(r[0], '%m/%d/%Y') 
    		r[0] = datetime.date(r[0].year,r[0].month,r[0].day)
    	else:
    		r[0] = None

    	if r[1] != '':												# converts mileage to integer, set to None if blank
    		r[1] = int(r[1])
    	else:
    		r[1] = None

    	if r[2] == '':												# sets location to None if blank. Already a string so no conversion needed
    		r[2] = None

    	if r[3] != '':												# converts gallons to float, set to None if blank
    		r[3] = float(r[3])
    	else:
    		r[3] = None

    	if r[4] != '':												# removes '$' from price string and converts to to float, set to None if blank
    		r[4] = float(r[4].replace('$',''))
    	else:
    		r[4] = None

    	rows.append(tuple(r));										# converts row to a tuple and adds to the list

    return rows  # a list of (date, mileage, location, gallons, price) tuples


# Exercise 1. (5 points)
#
def total_cost(rows):
    """Return the total amount of money spent on gas as a float.
    
    Hint: calculate by multiplying the price per gallon with the  number of gallons for each row.
    """
    total = 0.0  # delete this
    #
    # fill in function body here
    #
    for x in rows:												# Iterates over 'rows' list. Calculates total gas cost per entry if both values are present and adds it to the total
    	if x[3] != None and x[4] != None:				
    		gastotal = x[3] * x[4]
    		total += gastotal

    return round(total,2)


# Exercise 2. (5 points)
#
def num_single_locs(rows):
    """Return the number of refueling locations that were visited exactly once.
    
    Hint: store the locations and counts (as keys and values, respectively) in a dictionary, 
    then count up the number of entries with a value equal to one.  
    """
    num = 0  # delete this line!  
    #
    # fill in function body here
    #
    locations = {}
    for x in rows:												# Iterates through 'rows' list. Stores the count of occurences of a location in locations dictionary
    	if x[2] != None:
    		if x[2] in locations:
    			locations[x[2]] += 1
    		else:
    			locations[x[2]] = 1

    for i in locations.values():
    	if i == 1:
    		num += 1

    return num


# Exercise 3. (8 points)
#
def most_common_locs(rows):
    """Return a list of the 10 most common refueling locations, along with the number of times
    they appear in the data, in descending order.  
    
    Each list item should be a two-element tuple of the form (name, count).  For example, your
    function might return a list of the form: 
      [ ("Honolulu, HI", 42), ("Shermer, IL", 19), ("Box Elder, MO"), ... ]

    Hint: store the locations and counts in a dictionary as above, then convert the dictionary 
    into a list of tuples using the items() method.  Sort the list of tuples using sort() or 
    sorted().

    See:
      https://docs.python.org/3/tutorial/datastructures.html#dictionaries
      https://docs.python.org/3/howto/sorting.html#key-functions
    """
    #
    # fill in function body here
    #
    tempD = {}
    for x in rows:
    	if x[2] != None:							# Iterates through 'rows' stores valid locations in a dictionary
    		if x[2] in tempD:
    			tempD[x[2]] += 1
    		else:
    			tempD[x[2]] = 1

    locs = [(x,y) for x,y in tempD.items()]			# Converts the dictionary to a list of tuples and sorts it in descending order
    locs.sort(key=lambda x: x[1], reverse=True)

    return locs[0:10]								# Returns top 10 most visited locations

# Exercise 4. (8 points)
#
def state_totals(rows):
    """Return a dictionary containing the total number of visits (value) for each state as 
    designated by the two-letter abbreviation at the end of the location string (keys).  

    The return value should be a Python dictionary of the form:
      { "CA": 42, "HI": 19, "MA": 8675309, ... }

    Hint: to do this, you'll need to pull apart the location string and extract the state 
    abbreviation.  Note that some of the entries are malformed, and containing a state code but no
    city name.  You still want to count these cases (of course, if the location is blank, ignore
    the entry.
    """
    state__count = {}
    #
    # fill in function body here
    #
    for x in rows:
    	if x[2] != None:								# For each valid location string, extracts the state abbreviation and stores the count of occurrences in a dictionary
    		loc = x[2]
    		abbr = loc[len(loc)-2::]
    		if abbr in state__count:
    			state__count[abbr] += 1
    		else:
    			state__count[abbr] = 1

    return state__count


# Exercise 5. (8 points)
#
def num_unique_dates(rows):
    """Return the total number unique dates in the calendar that refueling took place.

    That is, if you ignore the year, how many different days had entries? (This number should be 
    less than or equal to 366!)
 
    Hint: the easiest way to do this is create a token representing the calendar day.  These could
    be strings (using strftime()) or integers (using date.toordinal()).  Store them in a Python set
    as you go, and then return the size of the set.

    See:
      https://docs.python.org/3/library/datetime.html#date-objects
    """
    #
    # fill in function body here
    #
    setdates = set()

    for x in rows:										#	Checks for valid dates in rows and converts the month and day to a string. Stores the string into a set and returns set size
    	if x[0] != None:
    		dateObj = x[0]
    		dateStr = dateObj.strftime("%m/%d")
    		setdates.add(dateStr)
    
    return len(setdates)


# Exercise 6. (8 points)
#
def month_avg_price(rows):
    """Return a dictionary containing the average price per gallon as a float (values) for each 
    month of the year (keys).

    The dictionary you return should have 12 entries, with full month names as keys, and floats as
    values.  For example:
        { "January": 3.12, "February": 2.89, ... }

    See:
      https://docs.python.org/3/library/datetime.html
    """
    monthly_avg = {}  
    testdict = {}
    #
    # fill in function body here
    #
    for x in rows:
    	if x[0] != None and x[4] != None:
    		dateObj = x[0]
    		dateStr = dateObj.strftime("%B")
    		if dateStr in testdict:
    			testdict[dateStr][0] += x[4]
    			testdict[dateStr][1] += 1
    		else:
    			testdict[dateStr] = [x[4],1]

    for month in testdict:
    	nums = testdict[month]
    	avg = nums[0] / nums[1]
    	monthly_avg[month] = avg

    #print(testdict)
    return monthly_avg


# EXTRA CREDIT (+10 points)
#
def highest_thirty(rows):
    """Return the start and end dates for top three thirty-day periods with the most miles driven.

    The periods should not overlap.  You should find them in a greedy manner; that is, find the
    highest mileage thirty-day period first, and then select the next highest that is outside that
    window).
    
    Return a list with the start and end dates (as a Python datetime object) for each period, 
    followed by the total mileage, stored in a tuple:  
        [ (1995-02-14, 1995-03-16, 502),
          (1991-12-21, 1992-01-16, 456),
          (1997-06-01, 1997-06-28, 384) ]
    """
    #
    # fill in function body here
    #
    thirty = []
    deltaMileage = 0
    firstDate = rows[0][0]
    lastDate = rows[len(rows)-1][0]
    delta = (lastDate - firstDate).days - 30
    leftEdgeDate = datetime.datetime(1900,1,1)     # This starts the 30 day window
    rightEdgeDate = datetime.datetime(1900,1,1)    # This is the end date of the 30 day window
    for t in range(30):
        deltaMileage = 0
        for i in range(delta):
            tmpLeftEdgeDate = firstDate + datetime.timedelta(days=i)   # Start date of current 30-day window
            tmpRightEdgeDate = tmpLeftEdgeDate + datetime.timedelta(days=30)    # End date of current 30-day window
            
            for tup in thirty:      # Must check if rightmost enters a date range that overlaps existing windows
                if((tmpRightEdgeDate >= tup[0]) & (tmpRightEdgeDate <= tup[1]) | (tmpLeftEdgeDate >= tup[0]) & (tmpLeftEdgeDate <= tup[1])):
                    tmpLeftEdgeDate = tup[1] + datetime.timedelta(days=1)
                    tmpRightEdgeDate = tmpLeftEdgeDate + datetime.timedelta(days=30)   # If we enter a range that already exists. Skip to just after the next window
            cnt = 0
            while(rows[cnt][0] < tmpLeftEdgeDate):   # While loop to find leftmost item (based on date)
                cnt+=1
                if(rows[cnt][0] == None):
                    cnt+=1
            while(rows[cnt][1] == None):     # While loop to mitigate the None mileages
                cnt+=1
            leftEdgeItem = rows[cnt]
            cnt = len(rows)-1
            while(rows[cnt][0] > tmpRightEdgeDate):  # While loop to find rightmost item (based on date)
                cnt-=1
                if(rows[cnt][0] == None):
                    cnt-=1
            while(rows[cnt][1] == None):      # While loop to mitigate the None mileages
                cnt-=1
            rightEdgeItem = rows[cnt]
            tmpDeltaMileage = rightEdgeItem[1] - leftEdgeItem[1]
            if(tmpDeltaMileage > deltaMileage):
                deltaMileage = tmpDeltaMileage
                leftEdgeDate = tmpLeftEdgeDate
                rightEdgeDate = tmpRightEdgeDate
        
        thirty.append([leftEdgeDate, rightEdgeDate, deltaMileage])
    
    return thirty


# The main() function below will be executed when your program is run.
# Note that Python does not require a main() function, but it is
# considered good style (as is including the __name__ == '__main__'
# conditional below)
#
def main(file_name):
    rows = read_data(file_name)
    print("Exercise 0: {} rows\n".format(len(rows)))

    cost = total_cost(rows)
    print("Exercise 1: ${:.2f}\n".format(cost))

    singles = num_single_locs(rows)
    print("Exercise 2: {}\n".format(singles))

    print("Exercise 3:")
    for loc, count in most_common_locs(rows):
        print("\t{}\t{}".format(loc, count))
    print("")

    print("Exercise 4:")
    for state, count in sorted(state_totals(rows).items()):
        print("\t{}\t{}".format(state, count))
    print("")

    unique_count = num_unique_dates(rows)
    print("Exercise 5: {}\n".format(unique_count))

    print("Exercise 6:")
    for month, price in sorted(month_avg_price(rows).items(),
                               key=lambda t: datetime.datetime.strptime(t[0], '%B').month):
        print("\t{}\t${:.2f}".format(month, price))
    print("")

    print("Extra Credit:")
    for start, end, miles in sorted(highest_thirty(rows)):
        print("\t{}\t{}\t{} miles".format(start.strftime("%Y-%m-%d"),
                                          end.strftime("%Y-%m-%d"), miles))
    print("")


#########################

if __name__ == '__main__':
    
    data_file_name = "mustard_data.csv" 
    main(data_file_name)




