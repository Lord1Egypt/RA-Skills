# Expression


## Overview
Informat uses `UEL` (Unified Expression Language) syntax for expressions. UEL is similar to JavaScript expressions in both syntax and semantics.
::: info Features
- No type conversion needed; conversion is usually done implicitly
- Double quotes and single quotes have the same usage
- `object.property` has the same meaning as `object['property']`
- Parts outside `${}` are returned as strings
:::


Here is a simple example of the Unified Expression Language:
::: info Object
``` javascript
let person = {
  name: '张三',
  age: 18
}
```
:::
:::: tabs

::: tab Example 1
```javascript
${person.name}
// Output
'张三'
```
:::

::: tab Example 2
```javascript
${person.age}
// Output
18
```
:::

::: tab Example 3
```javascript
${person.name}的年龄是${person.age}
// Output
'张三的年龄是18'
```
:::

::::
## Type Return
Expressions can directly declare and return variables
:::: tabs

::: tab Boolean
```javascript
${ true }
// Output
true
```
:::

::: tab Integer
```javascript
${ 123 }
// Output
123
```
:::
::: tab String
```javascript
${ '123' }
// Output
'123'
```
:::

::: tab Integer Array
```javascript
${ [1,2,3] }
// Output
[1,2,3]
```
:::
::: tab String Array
```javascript
${ ['1','2','3'] }
// Output
['1','2','3']
```
:::
::: tab Object
```javascript
${ {"prop1":1,"prop2":"str"}}
// Output
{"prop1":1,"prop2":"str"}
```
:::

::: tab Object Array
```javascript
${ [{"name","item1"},{"name","item2"}]}
// Output
[{"name","item1"},{"name","item2"}]
```
:::

::::

## String Concatenation
Expressions in Informat are executed either `on the client side` or `on the server side`. When executed on the client side, you can use `+` in expressions to concatenate strings with any object into a new string. For example:

:::: tabs

::: tab Example 1
```javascript
${'123' + '456'}
// Output
'123456'
```
:::

::: tab Example 2
```javascript
${'123' + 456}
// Output
'123456'
```
:::

::: tab Example 3
```javascript
${'a' + 4567}
// Output
'a4567'
```
:::

::: tab Example 4
```javascript
${1 + '' + 2}
// Output
'12'
```
:::

::::

::: warning Note
String concatenation using `+` is not supported when executed on the server side
```javascript
${'123'+'456'} //returns '579'
```
:::


If you need to perform string concatenation, use `String.concat(s1,s2)`
```javascript
${String.concat('123','456')} //returns '123456'
```

## Operators

::: info
- Arithmetic: +（addition）, - （subtraction）, *（multiplication）, /（division）, %(modulo)
- Logical: &&(and), ||(or), !（not）
- Relational: ==（equal）, !=（not equal）, <（less than）, >（greater than） <=（less than or equal）, >=（greater than or equal）
- Null: null（null value）
- Conditional: A ? B : C. Returns B or C, if A is true returns B, otherwise returns C
:::


## Reserved Keywords
Reserved keywords cannot be used as variable names
::: info Reserved Keywords
`and` `or` `not` `true` `false` `null` `empty` `div` `mod` `in` `matches` `eq`	`ne` `lt` `gt` `le`	`ge` `class`
:::

## Division by Zero Exception
In division operations, an exception will be thrown if the divisor is 0

## Operation Examples

| Expression      | Result  |
| -------------- | ------- |
| 1 > (4/2)      | false   |
| 4.0 >= 3       | true    |
| 100.0 == 100   | true    |
| (10*10) ne 100 | false   |
| 4 > 3          | true    |
| 1 + 2 > 2 - 1  | true    |
| 1 < 2 && 2 > 1 | true    |
| 1 < 2          | false   |
| 2 > 1          | true    |
| 'a' < 'b'      | true    |
| 1 + 2          | 3       |
| 1.2E4 + 1.4    | 12001.4 |
| 3 / 4        | 0.75    |
| 10 % 4       | 2       |

## Function Calls
Informat provides objects such as `Math` `Array` `Date` `Misc` `String` `User` `Encode` `Record` to handle function operations related to mathematical calculations, arrays, dates, etc. If an exception occurs during a function call, the system will roll back the current transaction. Here is an example of a function call:

```javascript
${Math.abs(-100)}//returns 100
```
