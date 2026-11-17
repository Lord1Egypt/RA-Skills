# Date

## Overview

Date operations. Includes date-related functions such as `Date.sysdate`, `Date.now` and `Date.dateSet`, as well as special notes about month and day-of-week value ranges.

**Special Notes**

Value range of month

| Month | Value |
|-----|----|
| January  | 0  |
| February  | 1  |
| March  | 2  |
| April  | 3  |
| May  | 4  |
| June  | 5  |
| July  | 6  |
| August  | 7  |
| September  | 8  |
| October | 9  |
| November | 10 |
| December | 11 |

Value range of day_of_week

| Day   | Value |
| ------ | ---- |
| Sunday | 0    |
| Monday | 1    |
| Tuesday | 2    |
| Wednesday | 3    |
| Thursday | 4    |
| Friday | 5    |
| Saturday | 6    |


## sysdate

Returns the current date and time

```javascript
Date.sysdate()
```

**Return Value**

Type `Date`
Current date and time

**Example**

```javascript
Date.sysdate() //Date object 
```

## now

Returns the UNIX timestamp of the current time

```javascript
Date.now()
```

**Return Value**

Type `Long`
UNIX timestamp of the current time

**Example**

```javascript
Date.now() // 1668483800328
```

## newDate

Returns a specified date

```javascript
Date.newDate(year, month, day, hour, minute, second, millisecond);
```

| Parameter | Type | Description |
|-------------|-----------|---------------------------------|
| year        | `Integer` | Year, optional or can be null, defaults to **current year** |
| month       | `Integer` | Month, optional or can be null, defaults to **January** |
| day         | `Integer` | Day, optional or can be null, defaults to **1** |
| hour        | `Integer` | Hour, optional or can be null, defaults to **0** |
| minute      | `Integer` | Minute, optional or can be null, defaults to **0** |
| second      | `Integer` | Second, optional or can be null, defaults to **0** |
| millisecond | `Integer` | Millisecond, optional or can be null, defaults to **0** |


**Return Value**

Type `Date` Returns the specified date

**Example**

```javascript
Date.newDate(); //Returns current date and time if no parameters
Date.newDate(null); //2025-01-01 00:00:00,000
Date.newDate(2022);// 2022-01-01 00:00:00,000
Date.newDate(2025, 0, 3); // 2025-01-03 00:00:00,000
Date.newDate(2025, 0, 1, 2, 3, 4, 5);// 2025-01-01 02:03:04,005
Date.newDate(2025, null, null); // 2025-01-01 00:00:00,000
Date.newDate(null, null, null, null, null, null, null, null); // 2025-01-01 00:00:00,000
Date.newDate(null, 0, 1, 2, 3, 4, 5, 6); // 2025-01-01 02:03:04,005
Date.newDate(null, 0, 1, null, 3, 4, 5); // 2025-01-01 00:03:04,005
```

## dateSet

Sets the specified type part of date d to value

```javascript
Date.dateSet(d, type, value)
```

| Parameter | Type | Description |
|-------|-----------|-----------------------|
| d     | `Date` or `Long` | Date or UNIX timestamp to compute |
| type  | `String`    | Operation type |
| value | `Integer`   | Value to set, defaults to 0 if null |

::: info
Possible values for type: `year:year`, `month:month`, `day:day_of_year`, `day of month:day_of_month`, `day of week:day_of_week`, `hour:hour`, `minute:minute`, `second:second`, `millisecond:millisecond`
:::

**Return Value**

Type `Date`
The computed date

**Example**

```javascript
//Assuming date value is 2022-11-01 00:00:00,000, timestamp is 1667232000000
Date.dateSet(date, 'year', 2024); //2024-11-01 00:00:00,000
Date.dateSet(date, 'year', null); //0001-11-01 00:00:00,000
Date.dateSet(date, 'year', -1); //0002-11-01 00:00:00,000
Date.dateSet(null, 'year', 2024); //null
Date.dateSet(date, null, 2024); //null
Date.dateSet(date, 'month', 1); //2022-02-01 00:00:00,000
Date.dateSet(date, 'day_of_year', 1); //2022-01-01 00:00:00,000
Date.dateSet(date, 'day_of_month', 1); //2022-11-01 00:00:00,000
Date.dateSet(date, 'day_of_week', 1); //2022-10-30 00:00:00,000
Date.dateSet(date, 'hour', 1); //2022-11-01 01:00:00,000
Date.dateSet(date, 'minute', 1); //2022-11-01 00:01:00,000
Date.dateSet(date, 'second', 1); //2022-11-01 00:00:01,000
Date.dateSet(date, 'millisecond', 1); //2022-11-01 00:00:00,001
Date.dateSet(timestamp, 'year', 2024); //2024-11-01 00:00:00,000
Date.dateSet(timestamp, 'month', 1); //2022-02-01 00:00:00,000
```


## dateAdd

Calculates the date by adding diff to date d according to type

```javascript
Date.dateAdd(d, type, diff)
```

| Parameter | Type | Description |
|------|-----------|-------------------------------------------|
| d    | Date or Long | Date or UNIX timestamp to compute |
| type | String    | Operation type |
| diff | Integer   | Value to add or subtract, defaults to 0 if null. Pass positive for addition, negative for subtraction |

::: info
Possible values for type: `year:year`, `month:month`, `day:day_of_year`, `day of month:day_of_month`, `day of week:day_of_week`, `hour:hour`, `minute:minute`, `second:second`, `millisecond:millisecond`
:::

**Return Value**

Type `Date`
The computed date

**Example**

```javascript
//Assuming date value is 2022-11-01 00:00:00,000, timestamp is 1667232000000
Date.dateAdd(date, 'year', 1); //2023-11-01 00:00:00,000
Date.dateAdd(date, 'year', null); //2022-11-01 00:00:00,000
Date.dateAdd(date, 'year', -1); //2021-11-01 00:00:00,000
Date.dateAdd(date, 'month', 1); //2022-12-01 00:00:00,000
Date.dateAdd(date, 'day_of_year', 1); //2022-11-02 00:00:00,000
Date.dateAdd(date, 'day_of_month', 1); //2022-11-02 00:00:00,000
Date.dateAdd(date, 'day_of_week', 1); //2022-11-02 00:00:00,000
Date.dateAdd(date, 'hour', 1); //2022-11-01 01:00:00,000
Date.dateAdd(date, 'minute', 1); //2022-11-01 00:01:00,000
Date.dateAdd(date, 'second', 1); //2022-11-01 00:00:01,000
Date.dateAdd(date, 'millisecond', 1); //2022-11-01 00:00:00,001
Date.dateAdd(timestamp, 'year', 2); //2024-11-01 00:00:00,000
Date.dateAdd(timestamp, 'month', 1); //2022-12-01 00:00:00,000
```



## datePart

Returns the specified type part of date d

```javascript
Date.datePart(d, type)
```

| Parameter | Type | Description |
|------|-----------|-----------------|
| d    | `Date` or `Long` | Date or UNIX timestamp to compute |
| type | `String`    | Operation type |

::: info
Possible values for type: `year:year`, `month:month`, `day:day_of_year`, `day of month:day_of_month`, `day of week:day_of_week`, `hour:hour`, `minute:minute`, `second:second`, `millisecond:millisecond`
:::

**Return Value**

Type `Integer`
The specified type part of date d

**Example**

```javascript
//Assuming date value is 2022-11-01 13:10:12,000, timestamp is 1667279412000
Date.datePart(date, 'year'); //2022
Date.datePart(date, 'month'); //10
Date.datePart(date, 'day_of_year'); //305
Date.datePart(date, 'day_of_month'); //1
Date.datePart(date, 'day_of_week'); //3
Date.datePart(date, 'hour'); //13
Date.datePart(date, 'minute'); //10
Date.datePart(date, 'second'); //12
Date.datePart(date, 'millisecond'); //0
Date.datePart(null, 'year'); //null
Date.datePart(date, null); //null
Date.datePart(timestamp, 'year'); //2022
Date.datePart(timestamp, 'month'); //10
Date.datePart(date, 'week_of_year'); //45
```



## dateBefore

Determines whether date d1 is before date d2

```javascript
Date.dateBefore(d1, d2)
```

| Parameter | Type | Description |
|----|-----------|-------------|
| d1 | `Date` or `Long` | Date 1 or UNIX timestamp |
| d2 | `Date` or `Long`| Date 2 or UNIX timestamp |

**Return Value**

Type `Boolean`
Whether date d1 is before date d2, returns false if d1 and d2 are equal

**Example**

```javascript
//Assuming date1 value is 2022-11-01 13:10:12,000, timestamp is 1667279412000
//Assuming date2 value is 2022-02-02 13:10:12,000, timestamp is 1643778612000

Date.dateBefore(date1, date2); //false
Date.dateBefore(date2, date1); //true
Date.dateBefore(timestamp1, timestamp2); //false
Date.dateBefore(timestamp2, timestamp1); //true
Date.dateBefore(timestamp1, date2); //false
Date.dateBefore(timestamp2, date1); //true
Date.dateBefore(date1, null); //false
Date.dateBefore(null, date2); //false
Date.dateBefore(timestamp1, null); //false
Date.dateBefore(null, timestamp2); //false
Date.dateBefore(null, null); //false
```



## dateAfter

Determines whether date d1 is after date d2

```javascript
Date.dateAfter(d1, d2)
```

| Parameter | Type | Description |
|----|-----------|-------------|
| d1 | `Date` or `Long` | Date 1 or UNIX timestamp |
| d2 | `Date` or `Long` | Date 2 or UNIX timestamp |

**Return Value**

Type `Boolean`
Whether date d1 is after date d2, returns false if d1 and d2 are equal

**Example**

```javascript
//Assuming date1 value is 2022-11-01 13:10:12,000, timestamp is 1667279412000
//Assuming date2 value is 2022-02-02 13:10:12,000, timestamp is 1643778612000

Date.dateAfter(date1, date2); //true
Date.dateAfter(date2, date1); //false
Date.dateAfter(timestamp1, timestamp2); //true
Date.dateAfter(timestamp2, timestamp1); //false
Date.dateAfter(timestamp1, date2); //true
Date.dateAfter(timestamp2, date1); //false
Date.dateAfter(date1, null); //false
Date.dateAfter(null, date2); //false
Date.dateAfter(timestamp1, null); //false
Date.dateAfter(null, timestamp2); //false
Date.dateAfter(null, null); //false
```



## dateDiff

Calculates the difference in days between two dates

```javascript
Date.dateDiff(d1, d2)
```

| Parameter | Type | Description |
|----|-----------|-------------|
| d1 | `Date` or `Long` | Date 1 or UNIX timestamp |
| d2 | `Date` or `Long` | Date 2 or UNIX timestamp |

**Return Value**

Type `Integer`
The difference in days between two dates. Returns 0 if equal, returns negative if d1 is before d2, otherwise returns positive

**Example**

```javascript
//Assuming date1 value is 2022-10-01 13:10:12, timestamp is 1667279412000
//Assuming date2 value is 2023-12-01 13:10:12, timestamp is 1701407412000

Date.dateDiff(date1, date2); //-426
Date.dateDiff(date2, date1); //426
Date.dateDiff(timestamp1, timestamp2); //-426
Date.dateDiff(timestamp2, timestamp1); //426
Date.dateDiff(timestamp1, date2); //-426
Date.dateDiff(timestamp2, date1); //426
Date.dateDiff(date1, null); //null
Date.dateDiff(null, date2); //null
Date.dateDiff(timestamp1, null); //null
Date.dateDiff(null, timestamp2); //null
Date.dateDiff(null, null); //null
```



## monthDiff

Calculates the difference in months between two dates

```javascript
Date.monthDiff(d1, d2)
```

| Parameter | Type | Description |
|----|-----------|-------------|
| d1 | `Date` or `Long` | Date 1 or UNIX timestamp |
| d2 | `Date` or `Long` | Date 2 or UNIX timestamp |

**Return Value**

Type `Integer`
The difference in months between two dates. Returns 0 if equal, returns negative if d1 is before d2, otherwise returns positive

**Example**

```javascript
//Assuming date1 value is 2022-10-01 13:10:12, timestamp is 1667279412000
//Assuming date2 value is 2023-12-01 13:10:12, timestamp is 1701407412000

Date.monthDiff(date1, date2); //-14
Date.monthDiff(date2, date1); //14
Date.monthDiff(timestamp1, timestamp2); //-14
Date.monthDiff(timestamp2, timestamp1); //14
Date.monthDiff(timestamp1, date2); //-14
Date.monthDiff(timestamp2, date1); //14
Date.monthDiff(date1, null); //null
Date.monthDiff(null, date2); //null
Date.monthDiff(timestamp1, null); //null
Date.monthDiff(null, timestamp2); //null
Date.monthDiff(null, null); //null
```



## weekDiff

Calculates the difference in weeks between two dates

```javascript
Date.weekDiff(d1, d2)
```

| Parameter | Type | Description |
|----|-----------|-------------|
| d1 | `Date` or `Long` | Date 1 or UNIX timestamp |
| d2 | `Date` or `Long`| Date 2 or UNIX timestamp |

**Return Value**

Type `Integer`
The difference in weeks between two dates. Returns 0 if equal, returns negative if d1 is before d2, otherwise returns positive

**Example**

```javascript
//Assuming date1 value is 2022-10-01 13:10:12, timestamp is 1667279412000
//Assuming date2 value is 2023-12-01 13:10:12, timestamp is 1701407412000

Date.weekDiff(date1, date2); //-60
Date.weekDiff(date2, date1); //60
Date.weekDiff(timestamp1, timestamp2); //-60
Date.weekDiff(timestamp2, timestamp1); //60
Date.weekDiff(timestamp1, date2); //-60
Date.weekDiff(timestamp2, date1); //60
Date.weekDiff(date1, null); //null
Date.weekDiff(null, date2); //null
Date.weekDiff(timestamp1, null); //null
Date.weekDiff(null, timestamp2); //null
Date.weekDiff(null, null); //null
```



## quarterDiff

Calculates the difference in quarters between two dates

```javascript
Date.quarterDiff(d1, d2)
```

| Parameter | Type | Description |
|----|-----------|-------------|
| d1 | `Date` or `Long` | Date 1 or UNIX timestamp |
| d2 | `Date` or `Long` | Date 2 or UNIX timestamp |

**Return Value**

Type `Integer`
The difference in quarters between two dates. Returns 0 if equal, returns negative if d1 is before d2, otherwise returns positive

**Example**

```javascript
//Assuming date1 value is 2022-10-01 13:10:12, timestamp is 1667279412000
//Assuming date2 value is 2023-12-01 13:10:12, timestamp is 1701407412000

Date.quarterDiff(date1, date2); //-4
Date.quarterDiff(date2, date1); //4
Date.quarterDiff(timestamp1, timestamp2); //-4
Date.quarterDiff(timestamp2, timestamp1); //4
Date.quarterDiff(timestamp1, date2); //-4
Date.quarterDiff(timestamp2, date1); //4
Date.quarterDiff(date1, null); //null
Date.quarterDiff(null, date2); //null
Date.quarterDiff(timestamp1, null); //null
Date.quarterDiff(null, timestamp2); //null
Date.quarterDiff(null, null); //null
```

## getStartOfDay

Gets the start time of the specified date (00:00:00.000)

```javascript
Date.getStartOfDay()
Date.getStartOfDay(date)
```

| Parameter | Type | Description |
|------|--------|------------------------|
| date | `Date` | Optional, specified date, defaults to current date |

**Return Value**

Type `Date` Start time of the specified date

**Example**

```javascript
Date.getStartOfDay() // 00:00:00.000 of current date
Date.getStartOfDay(new Date(2025-01-15 14:30:45)) // 2025-01-15 00:00:00.000
```

## getMonday

Gets the Monday of the week containing the specified date

```javascript
Date.getMonday()
Date.getMonday(date)
```

| Parameter | Type | Description |
|------|--------|------------------------|
| date | `Date` | Optional, specified date, defaults to current date |

**Return Value**

Type `Date` Monday of the week containing the specified date (00:00:00.000)

**Example**

```javascript
// Assuming current date is 2025-01-16 (Thursday)
Date.getMonday() // 2025-01-13 00:00:00.000 (this Monday)
Date.getMonday(new Date(2025-01-19)) // 2025-01-13 00:00:00.000 (Sunday returns previous week's Monday)
```

## getDateOfThisWeek

Gets the date of the specified day of this week

```javascript
Date.getDateOfThisWeek(week)
```

| Parameter | Type | Description |
|------|-----------|------------------------|
| week | `Integer` | Day of week, 1=Monday, 2=Tuesday, ..., 7=Sunday |

**Return Value**

Type `Date` Date of the specified day of this week (00:00:00.000)

**Example**

```javascript
// Assuming current date is 2025-01-16 (Thursday)
Date.getDateOfThisWeek(1) // 2025-01-13 00:00:00.000 (this Monday)
Date.getDateOfThisWeek(5) // 2025-01-17 00:00:00.000 (this Friday)
Date.getDateOfThisWeek(7) // 2025-01-19 00:00:00.000 (this Sunday)
```

## getStartOfMonth

Gets the start date of the month containing the specified date

```javascript
Date.getStartOfMonth()
Date.getStartOfMonth(date)
```

| Parameter | Type | Description |
|------|--------|------------------------|
| date | `Date` | Optional, specified date, defaults to current date |

**Return Value**

Type `Date` First day of the month containing the specified date (00:00:00.000)

**Example**

```javascript
Date.getStartOfMonth() // First day of current month
Date.getStartOfMonth(new Date(2025-03-15)) // 2025-03-01 00:00:00.000
```

## getStartOfYear

Gets the start date of the year containing the specified date

```javascript
Date.getStartOfYear()
Date.getStartOfYear(date)
```

| Parameter | Type | Description |
|------|--------|------------------------|
| date | `Date` | Optional, specified date, defaults to current date |

**Return Value**

Type `Date` First day of the year containing the specified date (00:00:00.000)

**Example**

```javascript
Date.getStartOfYear() // First day of current year
Date.getStartOfYear(new Date(2025-06-15)) // 2025-01-01 00:00:00.000
```

## isSameDay

Determines whether two dates are the same day

```javascript
Date.isSameDay(date1, date2)
```

| Parameter | Type | Description |
|-------|--------|------|
| date1 | `Date` | Date 1 |
| date2 | `Date` | Date 2 |

**Return Value**

Type `Boolean` Whether the two dates are the same day

**Example**

```javascript
Date.isSameDay(new Date(2025-01-15 10:30:00), new Date(2025-01-15 14:45:00)) // true
Date.isSameDay(new Date(2025-01-15), new Date(2025-01-16)) // false
```

## timestampToDate

Converts a timestamp to a date object

```javascript
Date.timestampToDate(timestamp)
```

| Parameter | Type | Description |
|----------|----------|-------------|
| timestamp | `Long` or `String` | UNIX timestamp |

**Return Value**

Type `Date` Date object, returns `null` if conversion fails

**Example**

```javascript
Date.timestampToDate(1700000000000) // Date object
Date.timestampToDate("1700000000000") // Date object
Date.timestampToDate(null) // null
```

## dateToTimestamp

Converts a date object to a timestamp

```javascript
Date.dateToTimestamp(date)
```

| Parameter | Type | Description |
|------|--------|------|
| date | `Date` | Date object |

**Return Value**

Type `Long` UNIX timestamp, returns `null` if date is `null`

**Example**

```javascript
Date.dateToTimestamp(new Date()) // Current timestamp
Date.dateToTimestamp(null) // null
```

## formatDate

Formats a date as a string

```javascript
Date.formatDate(date, format)
```

| Parameter | Type | Description |
|--------|----------|------------|
| date   | `Date` or `Long` | Date object or timestamp |
| format | `String` | Date format |

**Return Value**

Type `String` Formatted date string, returns `null` if parameters are invalid

**Example**

```javascript
Date.formatDate(new Date(), "yyyy-MM-dd") // "2025-01-15"
Date.formatDate(1700000000000, "yyyy/MM/dd HH:mm:ss") // "2023/11/14 21:13:20"
Date.formatDate(null, "yyyy-MM-dd") // null
```

## parseDate

Parses a string into a date object

```javascript
Date.parseDate(dateString, format)
```

| Parameter | Type | Description |
|------------|----------|--------|
| dateString | `String` | Date string |
| format     | `String` | Date format |

**Return Value**

Type `Date` Date object, returns `null` if parsing fails

**Example**

```javascript
Date.parseDate("2025-01-15", "yyyy-MM-dd") // Date object
Date.parseDate("2025/01/15 14:30:00", "yyyy/MM/dd HH:mm:ss") // Date object
Date.parseDate("invalid", "yyyy-MM-dd") // null
```
