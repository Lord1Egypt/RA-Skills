# informat.excel Excel File Operations

## Template Expressions

```text
 1. Space separated
 2. Ternary operation {{test ? obj:obj2}}
 3. n: indicates this cell is a numeric type {{n:}}
 4. le: represents length {{le:()}} used in if/else {{le:() > 8 ? obj1 : obj2}}
 5. fd: format date {{fd:(obj;yyyy-MM-dd)}}
 6. fn: format number {{fn:(obj;###.00)}}
 7. fe: iterate data, create row
 8. !fe: iterate data without creating row
 9. $fe: shift down and insert, shifts all rows below the current row down by .size() rows, then inserts
10. !if: delete current column {{!if:(test)}}
11. `''` (single quotes) represent constant values, e.g. `{{ '1' }}` outputs 1
12. &NULL& represents a space
13. ]] line break
```


### Numeric Type
By default, cell formats are string type. If you need to display the cell as a number, use the n: directive
```
 {{n: }}
```

**Example**
:::: tabs
::: tab "Template Data"
```json
{
  "str": "123",
  "num": 1
}
```
:::
::: tab "Expression"
```
{{n:str}} 
{{n:num}}
```
:::
::::


### Length
Returns the length of a list
```
{{ le: (array)}
```

**Example**

:::: tabs
::: tab "Template Data"
```json
{
    "users":[1,2,3,4]
}
```
:::
::: tab "Expression"
```
{{ le:(users) }}
```
:::
::::


### Format Date
Returns a formatted date
```
{{fd:(obj;yyyy-MM-dd)}}
```
**Example**
:::: tabs
::: tab "Template Data"
```js
{
  date:new Date()
}
```
:::
::: tab "Expression"
```
{{ fd:(date;yyyy-MM-dd) }}
```
:::
::::


### Format Number
Returns a formatted number
```
{{fn:(obj;###.00)}}
```

::: tip
- Placeholder `0`
    - If there are more digits than the actual number, the missing positions are filled with 0.
    - If there are fewer digits than the actual number: the integer part remains unchanged, the decimal part is rounded.
- Placeholder `#`
    - If there are more digits than the actual number, no change.
    - If there are fewer digits than the actual number: the integer part remains unchanged, the decimal part is rounded.
:::

**Example**

:::: tabs
::: tab "Template Data"
```json
{
  "number":123.456
}
```
:::
::: tab "Expression"
```
{{fn:(number;###.0)}} // 123.5
{{fn:(number;###.0000)}} // 123.4560
```
:::
::::





### Iterate Data

```
{{ fe:array }}
```

**Example**
:::: tabs
::: tab "Template Data"
```json
{
    "users":[
        {"id":1, "name":"张三"},
        {"id":2, "name":"李四"},
        {"id":3, "name":"王五"}
    ]
}
```
:::

::: tab "Expression"
```
{{fe:users t.id t.name }}
```
:::
::::

::: tip Other Loops
- `$fe:` shifts the rows below the current row in the template downward
- `!fe:` does not shift the rows below the current row in the template downward; the loop-inserted data will overwrite the rows below the current row.
- `#fe:` has similar syntax to fe:, the difference is that #fe loops horizontally. Note that the expressions must be on the same row
:::

### Picture

```
 {{ img }}
```
**Example**
:::: tabs
::: tab "Template Data"
```js
let img = informat.excel.createTemplatePicture({
  type:'file', // Local storage
  content:'path/img.jpg', // File path in local storage
  width:100, // Width
  height:100, // Height
});
```
:::

::: tab "Expression"
```
{{ img }}
```
:::
::::
