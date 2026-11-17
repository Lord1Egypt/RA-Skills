<!-- DOCKEY: expr-5d2a7 -->
# Informat Low-Code Platform Expression SDK Documentation

---

## Warning: [Mandatory Constraints for AI-Generated Expressions] -- All AI must read this section before generating expressions

> **This document describes the Informat platform's proprietary DSL expression language (based on UEL), not JavaScript, not TypeScript, not any general-purpose programming language.**
>
> AI must strictly follow the prohibition rules below when generating Informat expressions. **Violating any rule will cause expression parsing errors and runtime failures.**

### 🔥 Top Principle: `${}` Must Wrap an Entire Expression Statement

`${}` is an "evaluation boundary", not a "parameter interpolation placeholder". The most common mistake is to put `${}` around a function argument or operand position, which causes the expression to be treated as a string instead of being evaluated. **Before writing each expression, confirm that `${}` wraps a complete UEL statement (the entire function call, the entire arithmetic expression, the entire property access), not a fragment of one.**

```
❌  Array.of(${'1'})              outputs the string "Array.of(1)", not an array
✅  ${Array.of('1')}              evaluates to array: [1]

❌  String.concat(${a}, ${b})     outputs the string "String.concat(...,...)"
✅  ${String.concat(a, b)}        evaluates to the concatenated string

❌  ${taskRecord} != null         string comparison, always true
✅  ${taskRecord != null}         boolean comparison result
```

If, after removing `${}` from your expression, what remains is not a complete UEL expression (e.g. it contains bare `Array.of(`, `String.concat(`), then `${}` is positioned wrong.

### Absolutely Prohibited Items (the following syntax is illegal in Informat expressions)

| Prohibited Syntax | Reason | Correct Alternative |
|-----------|------|------------|
| `function(...) { ... }` | Informat expressions do not support defining functions | Use platform built-in functions, e.g., `String.concat()` |
| `() => ...` | Arrow functions are not supported | Use platform built-in functions |
| `var x = ...` / `let x = ...` / `const x = ...` | Variable declarations are not supported | Write expressions directly |
| `if (...) { ... } else { ... }` | if/else statement blocks are not supported | Use ternary operator `A ? B : C` |
| `for (...)` / `while (...)` | Loop statements are not supported | Use Array series functions |
| `new Date()` | The `new` keyword is not supported | Use `Date.sysdate()` |
| `new Array()` / `[...]` array literals | Array literals are not supported | Use `Array.of(...)` |
| `{ key: value }` object literals | Object literals are not supported | Use `Misc.newObject()` |
| `'A' + 'B'` string concatenation with + | + is only for numeric operations | Use `String.concat('A','B')` |
| `${...}` nested `${}` | Nesting is prohibited | Remove the inner `${}` |
| `Func(${arg})` placing `${}` at a parameter position | `${}` must wrap the **entire expression**, not just an argument | Rewrite as `${Func(arg)}` so `${}` wraps the whole function call |
| `Func(${'a'}, ${'b'})` wrapping each argument with `${}` separately | Same as above; `${}` is not allowed at parameter positions | Rewrite as `${Func('a','b')}` |
| `'prefix' + ${expr} + 'suffix'` joining string literals via `${}` | String literals should not sit outside `${}`, and `+` cannot concatenate strings | Rewrite as `${String.concat('prefix',expr,'suffix')}` or use `prefix${expr}suffix` (treated as a template string) |
| `return ...` | The return statement is not supported | The expression itself is the return value |
| `console.log(...)` | Debug statements are not supported | No alternative |
| `parseInt(...)` / `parseFloat(...)` global functions | JS global functions are not supported | Use `Misc.parseInt(...)` / `Misc.parseFloat(...)` |
| `Math.max(a, b)` comparing two values directly | Math functions only accept single parameters or lists | Use ternary operator `a > b ? a : b` |
| `JSON.stringify(...)` | JS global objects are not supported | Use `Misc.jsonStringify(...)` |
| `.length` property access | Property syntax for accessing length is not supported | Use `Array.length(list)` or `String.length(s)` |
| `array[0]` subscript access | Array subscript syntax is not supported | Use `Array.get(list, 0)` |
| `obj.key` accessing properties of unknown objects | Only context variable properties can be accessed | Use `Misc.prop(obj, 'key')` |

### Rules AI Must Follow When Generating Expressions

1. **Expressions must be wrapped in `${}`**; content outside `${}` is plain string output as-is
2. **`${}` must wrap a complete expression statement** — never put `${}` only around a function argument, an operand, or any other "fragment". Test: imagine `${}` as a pair of "evaluation boundaries" — content inside is evaluated as a UEL expression as a whole, content outside is plain string. Function calls, arithmetic, property access — all must be **entirely** inside `${}`.
   ```
   ❌ Wrong: Array.of(${'1'})         → outputs string "Array.of(1)", not an array
   ✅ Right: ${Array.of('1')}         → evaluates to array [1]

   ❌ Wrong: String.concat(${name}, '-', ${code})  → outputs string "String.concat(zhangsan, -, A01)"
   ✅ Right: ${String.concat(name, '-', code)}     → evaluates to string "zhangsan-A01"

   ❌ Wrong: ${taskRecord} != null      → string "[object] != null", always true
   ✅ Right: ${taskRecord != null}      → boolean true / false

   ❌ Wrong: ${a} + ${b}                → string concat to "1 + 2"
   ✅ Right: ${a + b}                   → numeric sum 3
   ```
3. **Only call functions explicitly listed in this document**; fabricating function names is strictly prohibited
4. **The only way to concatenate strings**: `${String.concat(s1, s2, ...)}` -- using `+` is prohibited
5. **The only way to construct arrays**: `Array.of(item1, item2, ...)` -- using `[...]` is prohibited
6. **Get current date**: `Date.sysdate()` -- using `new Date()` is prohibited
7. **The only way for conditional branching**: ternary operator `A ? B : C` -- using if/else is prohibited
8. **Operators must be inside `${}`**, e.g., `${taskRecord != null}` not `${taskRecord} != null`
9. **Raw values of option fields should not be quoted**, e.g., `inProgress` not `'inProgress'`

---

## 1. Overview

The Informat low-code platform provides an **Expression SDK** for dynamic computation and logic control in the following scenarios:

- Workflow (BPMN) node configuration, approvers, routing conditions
- Startup configuration, instance names, auto-completion conditions
- Automation rules
- Forms, dashboards, API return values
- Scripts and rule engines

---

## 2. Expression Execution Rules

Informat expressions use UEL (Unified Expression Language) syntax, which is syntactically and semantically similar to JavaScript expressions, **but it is NOT JavaScript syntax. There are strict DSL constraints, and no JavaScript statement structures (function declarations, variable declarations, loops, conditional statements, etc.) are supported.**

### 2.1 Expression and Template Rules

- Expressions are wrapped in `${}`
- **`${}` is an "evaluation boundary"**: content inside the boundary is evaluated as a complete UEL expression; content outside the boundary is returned as a plain string as-is
- **`${}` must wrap an entire expression statement** — never put `${}` only around a function argument, an operand, or any other "fragment":
   - ❌ Wrong: `Array.of(${'1'})` → outputs string `"Array.of(1)"` (the outer `Array.of(...)` is not inside `${}`, so it's a literal string)
   - ✅ Right: `${Array.of('1')}` → evaluates to array `[1]` (the entire function call is inside `${}`)
- A string can contain multiple `${}` expressions, but each `${}` must contain a complete, independent expression
- String concatenation does not support using `+`; you must use `${String.concat('123','456')}` which returns `'123456'`

### 2.2 Expression Rules (Mandatory)

**Rule 1: `${}` must wrap a complete expression statement (most important)**

`${}` is an "evaluation boundary", not an "interpolation placeholder". Content inside is evaluated as a complete UEL expression; content outside is plain string. This means: **any function call, arithmetic operation, or property access must be written entirely inside `${}` from start to end** — never put `${}` only around an argument or operand.

How to test: remove `${}` and check what remains. It should be a **syntactically complete UEL expression**; if what remains is a "half-baked function call" like `Array.of(1)` (because you put `${}` only at the parameter position), the whole expression is actually treated as a string.

```
❌ Wrong: Array.of(${'1'})
   → actual output: string "Array.of(1)"
   → reason: the Array.of(...) part is outside ${} and treated as a literal string; only '1' is evaluated

✅ Right: ${Array.of('1')}
   → actual evaluation: array [1]
   → reason: the entire Array.of('1') is inside ${} and treated as a function call

❌ Wrong: String.concat(${name}, '-', ${code})
   → actual output: "String.concat(zhangsan, -, A01)" (string)

✅ Right: ${String.concat(name, '-', code)}
   → actual evaluation: string "zhangsan-A01"

❌ Wrong: ${a} + ${b}
   → actual output: string "1 + 2" (each value is evaluated separately and joined with +)

✅ Right: ${a + b}
   → actual evaluation: numeric value 3
```

**Rule 2: Nesting `${}` inside `${}` is prohibited**
```
❌ Wrong: ${Record.getRecordOptionName('task', 'priority', ${taskItem.priority})}
✅ Right: ${Record.getRecordOptionName('task','priority',taskItem.priority)}
```

**Rule 3: Raw values of list select fields should not be quoted**
```
❌ Wrong: 'inProgress'
✅ Right: inProgress
```

**Rule 4: Operators must be inside `${}`**
```
❌ Wrong: ${taskRecord} != null
✅ Right: ${taskRecord != null}
```

**Rule 5: Only functions that exist in the documentation can be used; fabricating functions is prohibited**
```
❌ Wrong: ${new Date()}
✅ Right: ${Date.sysdate()}
```

**Rule 6: Any JavaScript statement structure is prohibited**
```
❌ Wrong: ${function() { return 'value'; }}
❌ Wrong: ${() => 'value'}
❌ Wrong: ${var x = 1; x + 1}
❌ Wrong: ${if (a > 0) { return a; } else { return 0; }}
✅ Right: ${a > 0 ? a : 0}
```

### 2.3 Mandatory String Concatenation Rules

In Informat expressions:

1. The `+` operator is **only allowed** for numeric operations (Integer / Double)
2. Using `+` for string concatenation is **strictly prohibited**, for example:
   - `${'A' + 'B'}` -- wrong
   - `${name + '-' + code}` -- wrong
3. String concatenation does not support \n for newlines:
   - Wrong example: ${String.concat('a','\n','b')}
   - Correct example: ${String.concat('a','
     ','b')}
4. All string concatenation **must** use:
   - `${String.concat('A','B')}` -- correct
   - `${String.concat(name,'-',code)}` -- correct

Expressions that violate this rule will be considered **illegal expressions**.

---

## 3. Operators

| Type | Symbol |
|------|------|
| Arithmetic | `+` (addition), `-` (subtraction), `*` (multiplication), `/` (division), `%` (modulo) |
| Logical | `&&` (and), `\|\|` (or), `!` (not) |
| Relational | `==` (equal), `!=` (not equal), `<` (less than), `>` (greater than), `<=` (less than or equal), `>=` (greater than or equal) |
| Null | `null` (null value) |
| Conditional | `A ? B : C`, returns B if A is true, otherwise returns C |

> Warning: The `+` operator is only for numeric values and cannot be used for string concatenation.

---

## 4. Reserved Keywords

```
and  or  not  true  false  null  empty  div  mod  in  matches
eq  ne  lt  gt  le  ge  class
```

> Warning: The above keywords cannot be used as variable names.

---

## 5. Division by Zero Exception

In division operations, if the divisor is 0, an exception will be thrown.

---

## 6. Array Usage Mandatory Rules

### 6.1 Array Literals [Absolutely Prohibited]

In Informat expressions, array / List literal syntax is **strictly prohibited**:

```
Wrong: ['a']
Wrong: ['a','b']
```

The above syntax will **cause an error directly** during parsing.

### 6.2 Correct Array Construction (The Only Allowed Way)

```
Correct: Array.of('a','b')
```

### 6.3 Examples

```
Wrong: ${Array.first(User.usersWithRole(['researcher']))}
Correct: ${Array.first(User.usersWithRole(Array.of('researcher')))}
```

---

## 7. Function Calls

Informat provides objects such as `Math`, `Array`, `Date`, `Misc`, `String`, `User`, `Encode`, and `Record` to handle mathematical operations, arrays, dates, and other function operations. If an exception occurs during a function call, the system will roll back the current transaction.

Example:
```
${Math.abs(-100)}  // Returns 100
```

> Warning: AI is strictly prohibited from calling functions that do not exist in this document when generating expressions. All function calls must be written in the form `ObjectName.functionName(parameters)`. Global functions do not exist (such as `parseInt()`, `isNaN()`, `Object.keys()`, etc. are all illegal).

---

### Functions - Array Collection Functions

#### Array.of(...item)
Converts multiple elements into an array

```
Array.of('x', 2, 3, 4)  // ["x",2,3,4]
```

#### Array.join(array, separator)
Joins the contents of the array together using the separator

| Parameter | Type | Description |
|------|------|------|
| array | `Array` | The array to join |
| separator | `String` | Separator |

**Return value**: Type `String`, returns the joined string

#### Array.length(list)
Returns the number of elements in list

#### Array.get(list, key)
Gets an element from the collection. If it is a List collection, key is an index integer from 0 to (len-1); if it is a Map collection, key is the key of the key-value pair. Throws an exception if out of range.

#### Array.set(list, key, value)
Sets the value of an element in the collection

#### Array.add(list, item)
Adds element item to the end of collection list

| Parameter | Type | Description |
|------|------|------|
| list | `Array` | The collection to add the element to |
| item | `Object` | The element to add |

**Return value**: Type `Array`, returns the collection with the added element

#### Array.remove(list, item)
Removes an element from the collection. If the collection is a Map type, item is the key

| Parameter | Type | Description |
|------|------|------|
| list | `Array` or `Map` | The collection to remove the element from |
| item | `Object` or `String` | The element to remove or the key of the element |

#### Array.removeAll(list, item)
Batch removes elements from the collection. If the collection is a Map type, item is the key

#### Array.isEmpty(list)
Checks whether list is an empty collection; returns `true` if list is `null` or has length 0, otherwise returns `false`

#### Array.isNotEmpty(list)
Checks whether list is not an empty collection; returns `false` if list is `null` or has length 0, otherwise returns `true`

#### Array.contains(list, item)
Checks whether list contains item

#### Array.containsAny(list1, list2)
Checks whether list1 contains any element from list2. Always returns `false` when list1 is null; always returns `true` when list2 is empty

#### Array.containsAll(list1, list2)
Checks whether list1 contains all elements from list2. Always returns `false` when list1 or list2 is empty

#### Array.map(list, key)
Returns a list of the key property values from list

#### Array.props(list, props)
Returns a new object list composed of the props property lists of elements in list

#### Array.transform(list, mapping)
Returns a new object list composed of elements in list mapped according to mapping

#### Array.concat(list1, list2)
Returns a new list with list1 and list2 concatenated together

#### Array.sort(list, key)
Sorts list by the key property

#### Array.distinct(list)
Returns list with duplicate elements removed

#### Array.reverse(list)
Returns list in reversed order

#### Array.repeat(element, count)
Generates an array of length count where every element is element

#### Array.sublist(list, fromIndex, toIndex)
Returns the portion of list from fromIndex to toIndex

#### Array.filter(list, key, value)
Filters items from list where the key property equals value

#### Array.shift(list)
Removes and returns the first element of list

#### Array.pop(list)
Removes and returns the last element of list

#### Array.sum(list)
Sums the elements of a numeric list

#### Array.avg(list)
Calculates the average of the elements of a numeric list

#### Array.max(list)
Returns the maximum value of a numeric list

#### Array.min(list)
Returns the minimum value of a numeric list

#### Array.first(list)
Returns the first element of list

#### Array.last(list)
Returns the last element of list

---

### Functions - Context Functions

Context functions represent environment parameters during execution.

#### Context.userId()
Returns the user ID of the current operation

#### Context.appId()
Returns the current application ID

#### Context.appEnvProp(propKey)
Returns the environment variable of the current application

#### Context.httpHeaders()
Returns the HTTP Headers of the current operation

#### Context.clipboardData()
Returns the data stored in the current application clipboard

> The application clipboard must be set via: the automation step "Set Application Clipboard" or the widget "Set Application Clipboard Data"

#### Context.weworkAccessToken()
Returns the WeCom AccessToken

#### Context.dingtalkAccessToken()
Returns the DingTalk AccessToken

#### Context.feishuAccessToken()
Returns the Feishu App AccessToken

#### Context.feishuTenantAccessToken()
Returns the Feishu Tenant AccessToken

#### Context.requestIp()
Returns the IP information of the current request

#### Context.hasAppPerm(permKey)
Checks whether the current user has the application permission with the identifier permKey

#### Context.hasModulePerm(moduleKey, permKey)
Checks whether the current user has the module permission with module identifier moduleKey and permission identifier permKey

---

### Functions - Date Functions

> Warning: Using `new Date()` is strictly prohibited. You must use `Date.sysdate()` to get the current date.

#### month Value Range

| Month | Value |
|------|---|
| January | 0 |
| February | 1 |
| March | 2 |
| April | 3 |
| May | 4 |
| June | 5 |
| July | 6 |
| August | 7 |
| September | 8 |
| October | 9 |
| November | 10 |
| December | 11 |

#### day_of_week Value Range

| Day | Value |
|----|---|
| Sunday | 0 |
| Monday | 1 |
| Tuesday | 2 |
| Wednesday | 3 |
| Thursday | 4 |
| Friday | 5 |
| Saturday | 6 |

#### Date.sysdate()
Returns the current date and time

#### Date.now()
Returns the current UNIX timestamp

#### Date.newDate(year, month, day, hour, minute, second, millisecond)
Returns the specified date

| Parameter | Type | Description |
|------|------|------|
| year | `Integer` | Year, optional, defaults to current year |
| month | `Integer` | Month, optional, defaults to January (value 0) |
| day | `Integer` | Day, optional, defaults to 1 |
| hour | `Integer` | Hour, optional, defaults to 0 |
| minute | `Integer` | Minute, optional, defaults to 0 |
| second | `Integer` | Second, optional, defaults to 0 |
| millisecond | `Integer` | Millisecond, optional, defaults to 0 |

#### Date.dateSet(d, type, value)
Sets the part of date d specified by type to value

#### Date.dateAdd(d, type, diff)
Calculates the date by adding diff to date d according to type

| Parameter | Type | Description |
|------|------|------|
| d | `Date` or `Long` | The date or UNIX timestamp to calculate |
| type | `String` | Operation type |
| diff | `Integer` | Value to add or subtract; positive to add, negative to subtract |

type values: `year` (year), `month` (month), `day_of_year` (day of year), `day_of_month` (day of month), `day_of_week` (day of week), `hour` (hour), `minute` (minute), `second` (second), `millisecond` (millisecond)

#### Date.datePart(d, type)
Returns the part of date d specified by type

| Parameter | Type | Description |
|------|------|------|
| d | `Date` or `Long` | The date or UNIX timestamp to calculate |
| type | `String` | Operation type (same as dateAdd) |

#### Date.dateBefore(d1, d2)
Checks whether date d1 is before date d2

#### Date.dateAfter(d1, d2)
Checks whether date d1 is after date d2

#### Date.dateDiff(d1, d2)
Calculates the number of days between two dates

#### Date.monthDiff(d1, d2)
Calculates the number of months between two dates

#### Date.weekDiff(d1, d2)
Calculates the number of weeks between two dates

#### Date.quarterDiff(d1, d2)
Calculates the number of quarters between two dates

---

### Functions - Encode Encryption/Decryption Functions

#### Encode.md5(s)
Returns the MD5 hash of string s

#### Encode.urlEncode(str)
URL-encodes the string str

#### Encode.urlDecode(str)
URL-decodes the string str

---

### Functions - Math Functions

> Warning: Using JavaScript's `Math` global object syntax (such as `Math.max(a,b)` to compare two values) is strictly prohibited. Informat Math function parameters differ from JavaScript. Please strictly follow this document.

#### Math.abs(x)
Returns the absolute value of x

#### Math.pow(d1, d2)
Returns d1 raised to the power of d2

#### Math.ceil(x)
Returns the smallest integer greater than or equal to x

#### Math.floor(x)
Returns the largest integer less than or equal to x

#### Math.random()
Returns a random number between 0 and 1

#### Math.sqrt(x)
Returns the square root of x

#### Math.round(n, digits)
Returns the number n rounded to digits decimal places

---

### Functions - Misc Utility Functions

> Warning: Using `JSON.stringify()`, `JSON.parse()`, and other JavaScript global methods is strictly prohibited. You must use `Misc.jsonStringify()` and `Misc.jsonParse()`.

#### Misc.jsonStringify(obj)
Converts object obj to a JSON string

#### Misc.jsonParse(str)
Converts string str to a JSON object

#### Misc.parseFloat(str)
Converts string str to a decimal number

#### Misc.parseInt(str)
Converts string str to an integer

#### Misc.timestampToDate(timestamp)
Converts a UNIX timestamp numeric value to a date type

#### Misc.dateToTimestamp(date)
Converts a date type to a UNIX timestamp numeric value

#### Misc.formatDate(date, fmt)
Converts the variable date to a string according to the format fmt (e.g., `yyyy-MM-dd HH:mm:ss,SSS`)

#### Misc.parseDate(str, fmt)
Converts str to a date according to the format fmt (e.g., `yyyy-MM-dd HH:mm:ss,SSS`)

#### Misc.host()
Returns the system's home page address

#### Misc.pinyin(str)
Returns the Chinese pinyin of string str

#### Misc.shortPinyin(str)
Returns the first letter of the pinyin of each Chinese character in string str

#### Misc.expectNotNull(obj, message)
Checks whether the object is null. If null, throws an exception with the message; otherwise returns the object

#### Misc.expectFirst(array, message)
Returns the first element of array. If array is empty, throws an exception with the message

#### Misc.expectLast(array, message)
Returns the last element of array. If array is empty, throws an exception with the message

#### Misc.invokeScript(script, func, ...args)
Calls a function in a script

#### Misc.invokeAutomatic(automaticId, ...args)
Calls an automation program

#### Misc.httpGet(url)
Accesses the url address via GET method and returns the request content

#### Misc.prop(object, key)
Retrieves the value of property key from object

#### Misc.props(object, props)
Retrieves a new object containing the properties listed in props from object

#### Misc.transform(object, mapping)
Returns a new object list composed of elements mapped according to mapping

#### Misc.appId()
Gets the ID of the current application

#### Misc.getAppIdByKey(key)
Queries the application ID under the team by application identifier

#### Misc.attachmentURL(tableKey, fieldKey, value)
Gets the access URL for an attachment

| Parameter | Type | Description |
|------|------|------|
| tableKey | `String` | Data table ID |
| fieldKey | `String` | Field ID |
| value | `String` | The id property from TableAttachment |

#### Misc.appResURL(appResId)
Gets the resource URL from the application resource library

#### Misc.websiteResURL(moduleKey, filePath)
Gets the resource URL of the application website module

#### Misc.eval(expression, context)
Executes the expression engine to replace template data using context variables

| Parameter | Type | Description |
|------|------|------|
| expression | `String` | Expression string |
| context | `Object` | Context variables |

Example:
```
Misc.eval('name', {"name":"informat"})           // 'name'
Misc.eval('${name}', {"name":"informat"})        // 'informat'
Misc.eval('${detail.age}', {"name":"informat","detail":{"age":12}})  // 12
```

#### Misc.safesql(sql, params)
Generates a safe complete SQL for an SQL with `?` placeholders

#### Misc.uuid16()
Generates a 16-character uuid string

#### Misc.uuid32()
Generates a 32-character uuid string

#### Misc.newObject()
Constructs an empty object

#### Misc.recordSql(sql, parameters)
Executes an SQL query on data table record lists. Only `SELECT` statements are allowed, and only data table module records can be queried

| Parameter | Type | Description |
|------|------|------|
| sql | `String` | SQL statement |
| parameters | `Array<Object>` | Parameter list |

**Return value**: Type `Array<Object>`, the query result set

Example:
```
Misc.recordSql('select id,name from task where status=?', Array.of('1'))
```

Return value example:
```json
[
   {"name": "Name", "id": "pht21vzu5ozps"},
   {"name": "333", "id": "1"}
]
```

---

### Functions - Record Data Table Functions

#### Record.getById(tableId, recordId)
Returns the queried data table record information

| Parameter | Type | Description |
|------|------|------|
| tableId | `String` | Data table identifier |
| recordId | `String` | Record ID |

**Return value**: Type `Object`, data table record information; returns `null` if not found

#### Record.getFieldValue(tableId, recordId, fieldId)
Returns the field value of a data table record

| Parameter | Type | Description |
|------|------|------|
| tableId | `String` | Data table identifier |
| recordId | `String` | Record ID |
| fieldId | `String` | Field identifier |

**Return value**: Type `Object`, field value; returns `null` if record does not exist, returns `null` if property does not exist, throws exception if data table does not exist

#### Record.getByField(tableId, fieldId, opt, value)
Filters data table record list by a single field

| Parameter | Type | Description |
|------|------|------|
| tableId | `String` | Data table identifier |
| fieldId | `String` | Filter field |
| opt | `String` | Operator, see `ConditionOpt` |
| value | `Object` | Filter condition value |

**Return value**: Type `Array<Record>`, returns up to 10000 records; returns empty array if no matching data; throws exception if data table does not exist

#### Record.getByFields(tableId, conditions)
Filters data table record list by multiple fields

| Parameter | Type | Description |
|------|------|------|
| tableId | `String` | Data table identifier |
| conditions | `Array` | Filter conditions |

**Return value**: Type `Array<Record>`, returns up to 10000 records

#### Record.getRecordOptionName(tableId, fieldId, value)
Returns the name of a single option value

| Parameter | Type | Description |
|------|------|------|
| tableId | `String` | Data table identifier |
| fieldId | `String` | Field identifier |
| value | `String` | Option value |

**Return value**: Type `String`, the name of the option value; returns the passed option value if it does not exist; throws exception if data table does not exist

#### Record.getRecordOptionNames(tableId, fieldId, valueList, join)
Returns the names of multiple option values joined together

| Parameter | Type | Description |
|------|------|------|
| tableId | `String` | Data table identifier |
| fieldId | `String` | Field identifier |
| valueList | `Array<String>` | Option value list |
| join | `String` | Join string |

**Return value**: Type `String`

#### Record.getRecordOptions(tableId, fieldId)
Returns the option value list

| Parameter | Type | Description |
|------|------|------|
| tableId | `String` | Data table identifier |
| fieldId | `String` | Field identifier |

**Return value**: Type `Array<Option>`; returns null if the field is not `List Select`/`Tree Select`/`Cascader Select`; throws exception if data table does not exist

#### Record.getRelationList(tableId, fieldId, recordId)
Returns the value of the data table relation list field

| Parameter | Type | Description |
|------|------|------|
| tableId | `String` | Data table identifier |
| fieldId | `String` | Field identifier |
| recordId | `String` | Record ID |

**Return value**: Type `Array<Record>`; returns empty array if the field is not `Relation List`; throws exception if data table does not exist

---

### Functions - String Functions

> Warning: Using `+` for string concatenation is strictly prohibited; you must use `String.concat()`. Using the `.length` property is strictly prohibited; you must use `String.length(s)`.

#### String.upper(s)
Converts all letters in the string to uppercase

#### String.lower(s)
Converts all letters in the string to lowercase

#### String.concat(s1, s2, ...)
Merges multiple strings into one string (**this is the only legal way to concatenate strings**)

#### String.lpad(s1, len, s2)
Pads string s1 at the beginning with string s2 until the string length reaches len

| Parameter | Type | Description |
|------|------|------|
| s1 | `String` | The string to pad |
| len | `Integer` | Total length |
| s2 | `String` | Padding character |

#### String.rpad(s1, len, s2)
Pads string s1 at the end with string s2 until the string length reaches len

| Parameter | Type | Description |
|------|------|------|
| s1 | `String` | The string to pad |
| s2 | `String` | Padding character |
| len | `Integer` | Total length |

#### String.trim(s)
Removes all whitespace characters from both sides of string s

#### String.replace(s, s1, s2)
Replaces the first occurrence of string s1 in string s with string s2

#### String.replaceAll(s, s1, s2)
Replaces all occurrences of string s1 in string s with string s2

#### String.substr(s, start, len)
Extracts len characters from string s starting at index position start

#### String.substring(s, start, end)
Extracts the substring of string s from position start to position end

#### String.indexOf(s, s2)
Gets the position of the first occurrence of character s2 in string s

#### String.lastIndexOf(s, s2)
Gets the position of the last occurrence of character s2 in string s

#### String.contains(s, s2)
Checks whether string s contains character s2

#### String.length(s)
Gets the length of string s (**using the `.length` property is strictly prohibited**)

#### String.startsWith(s, s2)
Checks whether string s starts with character s2

#### String.endsWith(s, s2)
Checks whether string s ends with character s2

#### String.match(regex, input)
Uses regular expression regex to validate whether input meets the requirement

| Parameter | Type | Description |
|------|------|------|
| regex | `String` | Regex pattern (regex shorthands starting with `\` such as `\w`, `\d` are not supported yet) |
| input | `String` | The content to match |

#### String.isEmpty(s)
Checks whether the input string s is empty (returns true for both null and blank strings)

```
String.isEmpty('')     // true
String.isEmpty(' ')    // true
String.isEmpty(null)   // true
```

#### String.isNotEmpty(s)
Checks whether the input string s is not empty

```
String.isNotEmpty(' a ')  // true
String.isNotEmpty('')     // false
String.isNotEmpty(' ')    // false
String.isNotEmpty(null)   // false
```

#### String.html2text(s)
Converts the HTML content of string s to text content (output after XSS filter processing)

---

### Functions - User Functions

#### User.usersWithRole(roleIdList)
Returns the user ID list of users who have any one of the roles in roleIdList

| Parameter | Type | Description |
|------|------|------|
| roleIdList | `Array<String>` | Role identifier array (must be constructed using `Array.of(...)`) |

#### User.usersWithDepartment(departmentIdList)
Returns the user ID list of users belonging to the departments in departmentIdList

| Parameter | Type | Description |
|------|------|------|
| departmentIdList | `Array<String>` | Department identifier array (must be constructed using `Array.of(...)`) |

#### User.superiorUsers(userId)
Returns the superior user ID list of userId

#### User.superiorUsersWithLevel(userId, level)
Returns the consecutive multi-level superior user ID list of userId

| Parameter | Type | Description |
|------|------|------|
| userId | `String` | The user ID to query superiors for |
| level | `Integer` | The number of superior levels to query |

#### User.subordinateUsers(userId)
Returns the subordinate user ID list of userId

#### User.subordinateUsersWithLevel(userId, level)
Returns the consecutive subordinate user ID list of userId

| Parameter | Type | Description |
|------|------|------|
| userId | `String` | The user ID to query subordinates for |
| level | `Integer` | Number of levels |

#### User.leaderOfDept(departmentId)
Returns the leader ID list of a single department

#### User.leaderOfDeptWithLevel(departmentId, level)
Returns the leader ID list of consecutive parent departments

#### User.leaderOfDeptList(departmentIdList)
Returns the leader ID list of multiple departments

#### User.parentOfDept(departmentId)
Returns the parent department ID

#### User.parentOfDeptList(departmentId)
Returns the parent department ID list

#### User.childrenOfDept(departmentId)
Returns all subordinate department ID list of a single department (recursively returns all child nodes)

#### User.childrenOfDeptList(departmentList)
Returns all subordinate department ID list of multiple departments

#### User.directChildrenOfDept(departmentId)
Returns the direct child department ID list

#### User.user(userId)
Returns a single UserInfo user information

#### User.userInfo(userId)
Returns a single UserInfo user information

#### User.deptList(departmentIdList)
Returns `Array<InformatDepartment>`, the department information list for departmentIdList departments

#### User.dept(deptId)
Returns a single InformatDepartment department information

---

### Functions - T Internationalization Functions

#### T.t(key)
Returns the internationalized text for the specified key

---

## 8. Model Definitions

### UserInfo User Information

| Field | Type | Description |
|------|------|------|
| userName | string | Username |
| mobileNo | string | Mobile number |
| email | string | Email |
| oid | string | OID |
| remark | string | Remark |
| id | string | User ID |
| name | string | User name |
| avatar | string | Avatar |
| roleList | Array&lt;string&gt; | Role list |
| departmentList | Array&lt;string&gt; | Department list |
| leaderList | Array&lt;string&gt; | Direct superior list |
| companyRoleList | Array&lt;string&gt; | Team role list |
| weworkUserId | string | WeCom account ID |
| dingtalkUserId | string | DingTalk account ID |
| feishuUserId | string | Feishu account ID |
| userInfo | object | Automation extended information |
| permissionList | Set | Permission list |

### InformatDepartment Department

| Field | Type | Description |
|------|------|------|
| id | string | Department unique identifier (OID) |
| name | string | Department name |
| shortName | string | Department short name |
| remark | string | Department description |
| parentId | string | Parent department ID (OID) |
| ownerList | List&lt;string&gt; | Department leader ID list |
| rowNumber | number | Sort order |
| isDisable | boolean | Whether disabled |

---

## Module Documentation Index

Detailed function documentation for each module is located under `./expression/` directory:

| Module | File | Description |
|------|------|------|
| Overview | `./expression/index.md` | Expression overview and basic syntax |
| Array | `./expression/array.md` | Array functions (of, contains, filter, map, etc.) |
| Context | `./expression/context.md` | Context functions (userId, appId, companyId, etc.) |
| Date | `./expression/date.md` | Date functions (now, format, addDays, etc.) |
| Encode | `./expression/encode.md` | Encoding/decoding functions (base64, md5, urlEncode, etc.) |
| Math | `./expression/math.md` | Math functions (abs, round, max, min, etc.) |
| Misc | `./expression/misc.md` | Miscellaneous functions |
| Record | `./expression/record.md` | Data record operation functions |
| String | `./expression/string.md` | String functions (concat, substring, replace, etc.) |
| User | `./expression/user.md` | User and department functions (usersWithRole, userInfo, userList, etc.) |
