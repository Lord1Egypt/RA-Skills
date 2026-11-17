# informat.date Date Operations

## Overview

Use the `informat.date` object to perform date-related operations

## format

Format a date

```javascript
informat.date.format(date, format)
```

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| date      | `Date`   | Date object       |
| format    | `String` | Format expression |

**Return Value**

Type `String`, the formatted string

**Example**

::: code-group

```javascript [Call]
informat.date.format(new Date(), 'yyyy-MM-dd HH:mm:ss')
```
```text [Return Value]
2023-05-09 11:04:48
```
:::

## parse

Parse a date from a string

```javascript
informat.date.parse(str, format)
```

| Parameter | Type     | Description       |
|-----------|----------|-------------------|
| str       | `String` | Date string       |
| format    | `String` | Format expression |

**Return Value**

Type `Date`, returns `null` if parsing fails

**Example**

::: code-group

```javascript [Call]
informat.date.parse('2023-05-09 11:04:48', 'yyyy-MM-dd HH:mm:ss')
```
```text [Return Value]
Tue May 09 11:04:48 CST 2023
```
:::


## parseDate

Parse a date from a string

```javascript
informat.date.parseDate(str)
```

| Parameter | Type     | Description  |
|-----------|----------|--------------|
| str       | `String` | Date string  |

**Return Value**

Type `Date`, returns `null` if parsing fails

**Example**

::: code-group

```javascript [Call]
informat.date.parseDate('2023-05-09 11:04:48')
informat.date.parseDate('2023-05-09 11:04')
informat.date.parseDate('2023-05-09 11')
informat.date.parseDate('2023-05-09')
informat.date.parseDate('2018-10-26T07:01:26Z')
informat.date.parseDate('1741337150957')

```
```text [Return Value]
Tue May 09 11:04:48 CST 2023 
Tue May 09 11:04:00 CST 2023 
Tue May 09 00:00:00 CST 2023 
Tue May 09 00:00:00 CST 2023 
Fri Oct 26 15:01:26 CST 2018 
Fri Mar 07 16:45:50 CST 2025
```
:::


## dateToTimestamp

Convert a date to a UNIX timestamp numeric value

```javascript
informat.date.dateToTimestamp(date)
```

| Parameter | Type | Description  |
|-----------|------|--------------|
| date      | Date | Date object  |

**Return Value**

Type `Integer`
The converted UNIX timestamp. Returns `null` if date is `null`

**Example**

::: code-group

```javascript [Call]
informat.date.dateToTimestamp(new Date())
```
```text [Return Value]
1667232000000
```
:::


## timestampToDate

Convert a UNIX timestamp numeric value to a date

```javascript
informat.date.timestampToDate(date)
```

| Parameter | Type    | Description    |
|-----------|---------|----------------|
| timestamp | Integer | UNIX timestamp |

**Return Value**

Type `Date`
The converted date. Returns `null` if timestamp is `null`

**Example**

::: code-group

```javascript [Call]
informat.date.timestampToDate(1667232000000)
```
```text [Return Value]
Tue Nov 01 00:00:00 CST 2022
```
:::


## getDateOfThisWeek

Get the date corresponding to a specific day of the current week

```javascript
informat.date.getDateOfThisWeek(dayOfWeek)
```

| Parameter | Type | Description                                |
|-----------|------|--------------------------------------------|
| dayOfWeek | int  | Day of the week, a number between 1 and 7  |

**Return Value**

Type `Date`

**Example**

::: code-group

```javascript [Call]
informat.date.getDateOfThisWeek(7)
```
```text [Return Value]
Tue Apr 06 00:00:00 CST 2025 
```
:::

## getMonday

Get Monday at 00:00:00.000 of the week containing the current date (hours, minutes, seconds, and milliseconds are all 0)

```javascript
informat.date.getMonday()
```


**Return Value**

Type `Date`

**Example**

::: code-group

```javascript [Call]
informat.date.getMonday()
```
```text [Return Value]
Mon Apr 21 00:00:00 CST 2025
```
:::



## getMonday

Get Monday at 00:00:00.000 of the week containing the specified date (hours, minutes, seconds, and milliseconds are all 0)

```javascript
informat.date.getMonday(date)
```

| Parameter | Type | Description  |
|-----------|------|--------------|
| date      | Date | Date object  |


**Return Value**

Type `Date`

**Example**

::: code-group

```javascript [Call]
informat.date.getMonday(new Date())
```
```text [Return Value]
Mon Apr 14 00:00:00 CST 2025
```
:::



## getStartOfDay

Get 00:00:00 of the current date

```javascript
informat.date.getStartOfDay()
```


**Return Value**

Type `Date`

**Example**

::: code-group

```javascript [Call]
informat.date.getStartOfDay()
```
```text [Return Value]
Tue Apr 06 00:00:00 CST 2025 
```
:::


## getStartOfDay

Get 00:00:00 of the specified date

```javascript
informat.date.getStartOfDay(date)
```

| Parameter | Type | Description  |
|-----------|------|--------------|
| date      | Date | Date object  |

**Return Value**

Type `Date`

**Example**

::: code-group

```javascript [Call]
informat.date.getStartOfDay(new Date())
```
```text [Return Value]
Tue Apr 06 00:00:00 CST 2025 
```
:::



## getStartOfMonth

Get the 1st day of the month containing the current date, e.g., May 1st at 00:00:00.000 (hours, minutes, seconds, and milliseconds are all 0)

```javascript
informat.date.getStartOfMonth()
```


**Return Value**

Type `Date`

**Example**

::: code-group

```javascript [Call]
informat.date.getStartOfMonth()
```
```text [Return Value]
Tue Apr 01 00:00:00 CST 2025 
```
:::


## getStartOfMonth

Get the 1st day of the month containing the specified date, e.g., May 1st at 00:00:00.000 (hours, minutes, seconds, and milliseconds are all 0)

```javascript
informat.date.getStartOfMonth(date)
```

| Parameter | Type | Description  |
|-----------|------|--------------|
| date      | Date | Date object  |

**Return Value**

Type `Date`

**Example**

::: code-group

```javascript [Call]
informat.date.getStartOfMonth(new Date())
```
```text [Return Value]
Tue Apr 01 00:00:00 CST 2025 
```
:::



## getStartOfYear

Get New Year's Day of the year containing the current date, e.g., January 1st, 2025 at 00:00:00.000 (hours, minutes, seconds, and milliseconds are all 0)

```javascript
informat.date.getStartOfYear()
```


**Return Value**

Type `Date`

**Example**

::: code-group

```javascript [Call]
informat.date.getStartOfYear()
```
```text [Return Value]
Wed Jan 01 00:00:00 CST 2025 
```
:::


## getStartOfYear

Get New Year's Day of the year containing the specified date, e.g., January 1st, 2025 at 00:00:00.000 (hours, minutes, seconds, and milliseconds are all 0)

```javascript
informat.date.getStartOfYear(date)
```

| Parameter | Type | Description  |
|-----------|------|--------------|
| date      | Date | Date object  |

**Return Value**

Type `Date`

**Example**

::: code-group

```javascript [Call]
informat.date.getStartOfYear(new Date())
```
```text [Return Value]
Wed Jan 01 00:00:00 CST 2025 
```
:::


## isSameDay

Check whether two dates are the same day

```javascript
informat.date.isSameDay(date1, date2)
```

| Parameter | Type | Description    |
|-----------|------|----------------|
| date1     | Date | Date object 1  |
| date2     | Date | Date object 2  |

**Return Value**

Type `Boolean`

**Example**

::: code-group

```javascript [Call]
informat.date.isSameDay(date1, date2)
```
```text [Return Value]
true
```
:::

## dateAdd

Date offset

```javascript
informat.date.dateAdd(d, type, value)
```

| Parameter | Type           | Description                                                                          |
|-----------|----------------|--------------------------------------------------------------------------------------|
| d         | Date or Long   | The date or UNIX timestamp to calculate                                               |
| type      | String         | Offset unit                                                                          |
| diff      | Integer        | Value to add or subtract. Defaults to 0 if null. Pass a positive number to add, negative to subtract |


::: info
Possible values for type: `year:year`, `month:month`, `day:day_of_year`, `day of month:day_of_month`, `day of week:day_of_week`, `hour:hour`, `minute:minute`, `second:second`, `millisecond:millisecond`
:::

**Return Value**

Type `Date`

**Example**

```javascript
// Assume date value is 2022-11-01 00:00:00,000, timestamp is 1667232000000
informat.date.dateAdd(date, 'year', 1); //2023-11-01 00:00:00,000
informat.date.dateAdd(date, 'year', null); //2022-11-01 00:00:00,000
informat.date.dateAdd(date, 'year', -1); //2021-11-01 00:00:00,000
informat.date.dateAdd(date, 'month', 1); //2022-12-01 00:00:00,000
informat.date.dateAdd(date, 'day_of_year', 1); //2022-11-02 00:00:00,000
informat.date.dateAdd(date, 'day_of_month', 1); //2022-11-02 00:00:00,000
informat.date.dateAdd(date, 'day_of_week', 1); //2022-11-02 00:00:00,000
informat.date.dateAdd(date, 'hour', 1); //2022-11-01 01:00:00,000
informat.date.dateAdd(date, 'minute', 1); //2022-11-01 00:01:00,000
informat.date.dateAdd(date, 'second', 1); //2022-11-01 00:00:01,000
informat.date.dateAdd(date, 'millisecond', 1); //2022-11-01 00:00:00,001
informat.date.dateAdd(timestamp, 'year', 2); //2024-11-01 00:00:00,000
informat.date.dateAdd(timestamp, 'month', 1); //2022-12-01 00:00:00,000
```

## dateBefore

Determine whether date d1 is before date d2

```javascript
informat.date.dateBefore(d1, d2)
```

| Parameter | Type             | Description                 |
|-----------|------------------|-----------------------------|
| d1        | `Date` or `Long` | Date 1 or UNIX timestamp    |
| d2        | `Date` or `Long` | Date 2 or UNIX timestamp    |

**Return Value**

Type `Boolean`
Whether date d1 is before date d2. Returns false if d1 and d2 are equal.

**Example**

```javascript
// Assume date1 value is 2022-11-01 13:10:12,000, timestamp is 1667279412000
// Assume date2 value is 2022-02-02 13:10:12,000, timestamp is 1643778612000

informat.date.dateBefore(date1, date2); //false
informat.date.dateBefore(date2, date1); //true
informat.date.dateBefore(timestamp1, timestamp2); //false
informat.date.dateBefore(timestamp2, timestamp1); //true
informat.date.dateBefore(timestamp1, date2); //false
informat.date.dateBefore(timestamp2, date1); //true
informat.date.dateBefore(date1, null); //false
informat.date.dateBefore(null, date2); //false
informat.date.dateBefore(timestamp1, null); //false
informat.date.dateBefore(null, timestamp2); //false
informat.date.dateBefore(null, null); //false
```


## datePart

Return the specified part of date d

```javascript
informat.date.datePart(d, type)
```

| Parameter | Type             | Description                    |
|-----------|------------------|--------------------------------|
| d         | `Date` or `Long` | The date or UNIX timestamp     |
| type      | `String`         | Operation type                 |

::: info
- Possible values for type: `year:year`, `month:month`, `day:day_of_year`, `day of month:day_of_month`, `day of week:day_of_week`, `hour:hour`, `minute:minute`, `second:second`, `millisecond:millisecond`
- ***month*** is zero-based. For example, if date is November, informat.date.datePart(date, 'month'); returns 10
:::

**Return Value**

Type `Integer`
The specified part of date d

**Example**

```javascript
// Assume date value is 2022-11-01 13:10:12,000, timestamp is 1667279412000
informat.date.datePart(date, 'year'); //2022
informat.date.datePart(date, 'month'); //10
informat.date.datePart(date, 'day_of_year'); //305
informat.date.datePart(date, 'day_of_month'); //1
informat.date.datePart(date, 'day_of_week'); //3
informat.date.datePart(date, 'hour'); //13
informat.date.datePart(date, 'minute'); //10
informat.date.datePart(date, 'second'); //12
informat.date.datePart(date, 'millisecond'); //0
informat.date.datePart(null, 'year'); //null
informat.date.datePart(date, null); //null
informat.date.datePart(timestamp, 'year'); //2022
informat.date.datePart(timestamp, 'month'); //10
informat.date.datePart(date, 'week_of_year'); //45
```
