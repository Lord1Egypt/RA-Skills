# Math

## Overview

Mathematical operations. Includes mathematical functions such as `Math.abs`, `Math.pow`, `Math.ceil`, `Math.random`, `Math.sqrt` and `Math.round`



## abs

Returns the absolute value of x

```javascript
Math.abs(x)
```

| Parameter | Type | Description |
|----|-----------------|------------|
| x  | Integer or Double | Number to calculate absolute value of |

**Return Value**

Type `Integer` or `Double`
The absolute value of number x

**Example**

```javascript
Math.abs(-100.3) //100.3
```



## pow

Returns d1 raised to the power of d2

```javascript
Math.pow(d1, d2)
```

| Parameter | Type | Description |
|----|-----------------|-------------|
| d1 | `Integer` or `Double` | Number to raise to a power |
| d2 | `Integer` or `Double` | Exponent |

**Return Value**

Type `Double`
d1 raised to the power of d2

**Example**

```javascript
Math.pow(2, 3) //8.0
```


## ceil

Returns the smallest integer greater than or equal to x

```javascript
Math.ceil(x)
```

| Parameter | Type | Description |
|----|--------|-------|
| x  | `Double` | Number to compare |

**Return Value**

Type `Double`
The smallest integer greater than or equal to x


::: tip
- Note that the return value type is decimal
:::

**Example**

```javascript
Math.ceil(2.2) //3.0
```


## floor

Returns the largest integer less than or equal to x

```javascript
Math.floor(x)
```

| Parameter | Type | Description |
|----|--------|-------|
| x  | `Double` | Number to compare |

**Return Value**

Type `Double`
The largest integer less than or equal to x


::: tip
- Note that the return value type is decimal
:::

**Example**

```javascript
Math.floor(2.2) //2
```


## random

Returns a random number between 0 and 1

```javascript
Math.random()
```

**Return Value**

Type `Double`
A decimal greater than or equal to 0 and less than 1, returns a random number on each call

**Example**

```javascript
Math.random() //0.6260832016946124 
```



## sqrt

Returns the square root of x

```javascript
Math.sqrt(x)
```

| Parameter | Type | Description |
|----|--------|-----------|
| x  | `Double` | Number to find the square root of |

**Return Value**

Type `Double`
The square root of x

**Example**

```javascript
Math.sqrt(4) //2.0
```



## round

Returns the value of number n rounded to the specified number of digits

```javascript
Math.round(n, digits)
```

| Parameter | Type | Description |
|--------|---------|---------|
| n      | `Double`  | Number to round |
| digits | `Integer` | Number of decimal places for precision |

**Return Value**

Type `Double`
The rounded value

**Example**

```javascript
Math.round(3.1415926, 2)//3.14
Math.round(3.1415926, 4)//3.1416
```
