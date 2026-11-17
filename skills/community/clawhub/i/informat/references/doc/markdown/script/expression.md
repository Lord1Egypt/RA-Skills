# Expression Functions

## Overview

Informat provides the ability to call expression methods in scripts. The supported expressions are:

| Category | Description        | Notes                                |
|----------|--------------------|--------------------------------------|
| Array    | Collection         | Array collection related functions   |
| Date     | Date               | Date operation related functions     |
| Encode   | Character encoding | String encoding/decoding functions   |
| Math     | Number             | Mathematical operations              |
| Misc     | Other              | Other utility functions              |
| String   | String             | String related functions             |
| User     | User               | User related operation functions in the current system |
| Context  | Context            | Context related functions. Context represents environment parameters during execution |
| Record   | Data table record  | Data table related functions         |
| T        | Internationalization | Internationalization related functions |

## Array

Array collection related functions. Call via `informat.Array.method`

| Method | Parameters | Return Value | Description | Example |
|------|------|--------|------------------|------------|
| **of** | `...item: Object` | `Array<Object>` | Convert multiple elements to an array | `informat.Array.of('x', 2, 3) // ["x",2,3]` |
| **toList** | `item: Object` | `Array<Object>` | Convert element to array, clone if already array | `informat.Array.toList('x') // ["x"]` |
| **join** | `array: Array, separator: String` | `String` | Join array contents with separator | `informat.Array.join([1,2,3], '-') // "1-2-3"` |
| **length** | `list: Array` | `Integer` | Return array length, 0 for null | `informat.Array.length([1,2,3]) // 3` |
| **get** | `list: Array\|Map, key: Integer\|String` | `Object` | Get element at specified position in collection | `informat.Array.get([{name:'张三'}], 0) // {name:'张三'}` |
| **set** | `list: Array\|Map, key: String\|Integer, value: Object` | `Array\|Map` | Set element value in collection | `informat.Array.set({name:'张三'}, 'name', '李四')` |
| **add** | `list: Array, item: Object` | `Array` | Add element to end of array | `informat.Array.add([1,2], 3) // [1,2,3]` |
| **remove** | `list: Array\|Map, item: Object\|String` | `Array\|Map` | Remove element from collection (first match only) | `informat.Array.remove([1,2,3], 2) // [1,3]` |
| **removeAll** | `list: Array\|Map, item: Object\|String\|Array` | `Array\|Map` | Remove all matching elements from collection | `informat.Array.removeAll([1,2,2,3], 2) // [1,3]` |
| **isEmpty** | `list: Array\|Map` | `Boolean` | Check if collection is empty | `informat.Array.isEmpty([]) // true` |
| **isNotEmpty** | `list: Array\|Map` | `Boolean` | Check if collection is not empty | `informat.Array.isNotEmpty([1]) // true` |
| **contains** | `list: Array\|Map, item: Object` | `Boolean` | Check if collection contains specified element | `informat.Array.contains([1,2,3], 2) // true` |
| **containsAny** | `list1: Array, list2: Array` | `Boolean` | Check if list1 contains any element from list2 | `informat.Array.containsAny([1,2],[2,3]) // true` |
| **containsAll** | `list1: Array, list2: Array` | `Boolean` | Check if list1 contains all elements from list2 | `informat.Array.containsAll([1,2,3],[1,2]) // true` |
| **map** | `list: Array, key: String` | `Array` | Return list of specified property from each element | `informat.Array.map([{name:'张三'}], 'name') // ["张三"]` |
| **props** | `list: Array, props: Array<String>` | `Array` | Return new object list with specified properties | `informat.Array.props([{name:'张三'}], ['name']) // [{name:'张三'}]` |
| **transform** | `list: Array, mapping: Map<String,String>` | `Array` | Transform object properties by mapping | `informat.Array.transform([{name:'张三'}], {name:'userName'})` |
| **concat** | `list1: Array, list2: Array` | `Array` | Concatenate two arrays | `informat.Array.concat([1,2],[3,4]) // [1,2,3,4]` |
| **sort** | `list: Array, key: String` | `Array` | Sort array by specified property | `informat.Array.sort([{age:20},{age:18}], 'age')` |
| **distinct** | `list: Array` | `Array` | Remove duplicate items from array | `informat.Array.distinct([1,2,2,3]) // [1,2,3]` |
| **reverse** | `list: Array` | `Array` | Reverse array order | `informat.Array.reverse([1,2,3]) // [3,2,1]` |
| **repeat** | `count: Integer, element: Object` | `Array` | Generate array of repeated elements | `informat.Array.repeat(3, 'a') // ["a","a","a"]` |
| **sublist** | `list: Array, fromIndex: Integer, toIndex: Integer` | `Array` | Return subset of array | `informat.Array.sublist([1,2,3,4], 1, 2) // [2,3]` |
| **filter** | `list: Array, key: String, value: Object` | `Array` | Filter elements by specified property value | `informat.Array.filter([{a:1},{a:2}], "a", 2) // [{a:2}]` |
| **shift** | `list: Array` | `Object` | Remove and return first element of array | `informat.Array.shift([1,2,3]) // 1` |
| **pop** | `list: Array` | `Object` | Remove and return last element of array | `informat.Array.pop([1,2,3]) // 3` |
| **sum** | `list: Array` | `Double` | Sum a numeric array | `informat.Array.sum([1,2,3]) // 6.0` |
| **avg** | `list: Array` | `Double` | Average a numeric array | `informat.Array.avg([1,2,3]) // 2.0` |
| **max** | `list: Array` | `Double` | Get maximum of numeric array | `informat.Array.max([1,2,3]) // 3.0` |
| **min** | `list: Array` | `Double` | Get minimum of numeric array | `informat.Array.min([1,2,3]) // 1.0` |
| **first** | `list: Array` | `Object` | Return first element of array | `informat.Array.first([1,2,3]) // 1` |
| **last** | `list: Array` | `Object` | Return last element of array | `informat.Array.last([1,2,3]) // 3` |

## Date

Date operation related functions. Call via `informat.Date.method`

| Method | Parameters | Return Value | Description | Example |
|------|------|--------|------------------|------------|
| **sysdate** | No parameters | `Date` | Return current date and time | `informat.Date.sysdate() // Date object` |
| **now** | No parameters | `Long` | Return UNIX timestamp of current time | `informat.Date.now() // 1668483800328` |
| **newDate** | `year, month, day, hour, minute, second, millisecond` (all Integer, optional) | `Date` | Return specified date, parameters are optional | `informat.Date.newDate(2025, 0, 3) // 2025-01-03 00:00:00,000` |
| **dateSet** | `d: Date or Long, type: String, value: Integer` | `Date` | Set specified part of date to value | `informat.Date.dateSet(date, 'year', 2024) // Set year to 2024` |
| **dateAdd** | `d: Date or Long, type: String, diff: Integer` | `Date` | Calculate date after adding diff by type | `informat.Date.dateAdd(date, 'year', 1) // Add 1 year` |
| **datePart** | `d: Date or Long, type: String` | `Integer` | Return specified part of date | `informat.Date.datePart(date, 'year') // Return year` |
| **dateBefore** | `d1: Date or Long, d2: Date or Long` | `Boolean` | Determine if d1 is before d2 | `informat.Date.dateBefore(date1, date2) // true/false` |
| **dateAfter** | `d1: Date or Long, d2: Date or Long` | `Boolean` | Determine if d1 is after d2 | `informat.Date.dateAfter(date1, date2) // true/false` |
| **dateDiff** | `d1: Date or Long, d2: Date or Long` | `Integer` | Calculate day difference between two dates | `informat.Date.dateDiff(date1, date2) // Day difference` |
| **monthDiff** | `d1: Date or Long, d2: Date or Long` | `Integer` | Calculate month difference between two dates | `informat.Date.monthDiff(date1, date2) // Month difference` |
| **weekDiff** | `d1: Date or Long, d2: Date or Long` | `Integer` | Calculate week difference between two dates | `informat.Date.weekDiff(date1, date2) // Week difference` |
| **quarterDiff** | `d1: Date or Long, d2: Date or Long` | `Integer` | Calculate quarter difference between two dates | `informat.Date.quarterDiff(date1, date2) // Quarter difference` |

**Special Notes**

month value range

| Month     | Value |
|-----------|-------|
| January   | 0     |
| February  | 1     |
| March     | 2     |
| April     | 3     |
| May       | 4     |
| June      | 5     |
| July      | 6     |
| August    | 7     |
| September | 8     |
| October   | 9     |
| November  | 10    |
| December  | 11    |

day_of_week value range

| Day       | Value |
|-----------|-------|
| Sunday    | 0     |
| Monday    | 1     |
| Tuesday   | 2     |
| Wednesday | 3     |
| Thursday  | 4     |
| Friday    | 5     |
| Saturday  | 6     |

## Encode

String encoding/decoding related functions. Call via `informat.Encode.method`

| Method | Parameters | Return Value | Description | Example |
|------|------|--------|------------------|------------|
| **md5** | `s: String` | `String` | Return MD5 hash of string | `informat.Encode.md5('123456') // e10adc3949ba59abbe56e057f20f883e` |
| **urlEncode** | `str: String` | `String` | URL encode a string | `informat.Encode.urlEncode('https://next.informat.cn') // https%3A%2F%2Fnext.informat.cn` |
| **urlDecode** | `str: String` | `String` | URL decode a string | `informat.Encode.urlDecode('https%3A%2F%2Fnext.informat.cn') // https://next.informat.cn` |

## Math

Mathematical operations. Includes mathematical functions. Call via `informat.Math.method`

| Method | Parameters | Return Value | Description | Example |
|------|------|--------|------------------|------------|
| **abs** | `x: Integer or Double` | `Integer or Double` | Return absolute value of number | `informat.Math.abs(-100.3) // 100.3` |
| **pow** | `d1: Integer or Double, d2: Integer or Double` | `Double` | Return d1 raised to the power of d2 | `informat.Math.pow(2, 3) // 8.0` |
| **ceil** | `x: Double` | `Double` | Return smallest integer greater than or equal to x | `informat.Math.ceil(2.2) // 3.0` |
| **floor** | `x: Double` | `Double` | Return largest integer less than or equal to x | `informat.Math.floor(2.2) // 2.0` |
| **random** | No parameters | `Double` | Return random number between 0 and 1 | `informat.Math.random() // 0.6260832016946124` |
| **sqrt** | `x: Double` | `Double` | Return square root of x | `informat.Math.sqrt(4) // 2.0` |
| **round** | `n: Double, digits: Integer` | `Double` | Return number rounded to specified decimal places | `informat.Math.round(3.1415926, 2) // 3.14` |

## Misc

Utility functions. Call via `informat.Misc.method`

| Method | Parameters | Return Value | Description | Example |
|------|------|--------|------------------|------------|
| **jsonStringify** | `obj: Object` | `String` | Convert object to JSON string | `informat.Misc.jsonStringify({a:1}) // "{\"a\":1}"` |
| **jsonParse** | `str: String` | `Object` | Convert JSON string to object | `informat.Misc.jsonParse('{"a":1}') // {a:1}` |
| **parseFloat** | `str: String` | `Double` | Convert string to decimal | `informat.Misc.parseFloat("3.14") // 3.14` |
| **parseInt** | `str: String` | `Integer` | Convert string to integer | `informat.Misc.parseInt("3.14") // 3` |
| **timestampToDate** | `timestamp: Integer` | `Date` | Convert UNIX timestamp to date | `informat.Misc.timestampToDate(1667232000000)` |
| **dateToTimestamp** | `date: Date` | `Integer` | Convert date to UNIX timestamp | `informat.Misc.dateToTimestamp(new Date())` |
| **formatDate** | `date: Date, fmt: String` | `String` | Format date by format string | `informat.Misc.formatDate(date, 'yyyy-MM-dd')` |
| **parseDate** | `str: String, fmt: String` | `Date` | Parse date string by format | `informat.Misc.parseDate('2022-11-01', 'yyyy-MM-dd')` |
| **host** | No parameters | `String` | Return system homepage URL | `informat.Misc.host() // https://next.informat.cn/` |
| **pinyin** | `str: String` | `String` | Return Chinese pinyin of string | `informat.Misc.pinyin('你好') // "ni hao"` |
| **shortPinyin** | `str: String` | `String` | Return pinyin initials | `informat.Misc.shortPinyin('你好') // "nh"` |
| **expectNotNull** | `obj: Object, message: String` | `Object` | Null check, throw exception if null | `informat.Misc.expectNotNull(obj, 'cannot be null')` |
| **expectFirst** | `array: Array, message: String` | `Object` | Return first element of array | `informat.Misc.expectFirst([1,2], 'empty array') // 1` |
| **expectLast** | `array: Array, message: String` | `Object` | Return last element of array | `informat.Misc.expectLast([1,2], 'empty array') // 2` |
| **invokeScript** | `script: String, func: String, ...args: Object` | `Object` | Call a function in a script | `informat.Misc.invokeScript('test.js', 'add', 1, 2)` |
| **invokeAutomatic** | `automaticId: String, ...args: Object` | `Object` | Call an automation program | `informat.Misc.invokeAutomatic('test', 1, 2)` |
| **httpGet** | `url: String` | `String` | Access URL via GET method | `informat.Misc.httpGet('https://example.com')` |
| **prop** | `object: Object, key: String` | `Object` | Get object property value | `informat.Misc.prop({a:1}, 'a') // 1` |
| **props** | `object: Object, props: Array<String>` | `Object` | Get multiple properties as new object | `informat.Misc.props({a:1,b:2}, ['a'])` |
| **transform** | `object: Object, mapping: Map<String,String>` | `Object` | Transform object properties by mapping | `informat.Misc.transform({name:'张三'}, {name:'userName'})` |
| **appId** | No parameters | `String` | Get the current application ID | `informat.Misc.appId()` |
| **getAppIdByKey** | `key: String` | `String` | Query application ID by application identifier | `informat.Misc.getAppIdByKey('appKey')` |
| **attachmentURL** | `tableKey: String, fieldKey: String, value: String` | `String` | Get attachment access URL | `informat.Misc.attachmentURL('staff','photo','1.png')` |
| **appResURL** | `appResId: String` | `String` | Get application resource library resource URL | `informat.Misc.appResURL('image.jpg')` |
| **websiteResURL** | `moduleKey: String, filePath: String` | `String` | Get website module resource URL | `informat.Misc.websiteResURL('module','logo.png')` |
| **barcodeURL** | `value: String, format: String` | `String` | Return barcode image BASE64 value | `informat.Misc.barcodeURL('12345','CODE128')` |
| **qrcodeURL** | `value: String, width: Integer` | `String` | Return QR code image BASE64 value | `informat.Misc.qrcodeURL('text', 300)` |
| **eval** | `str: String, context: Object` | `Object` | Execute expression engine template replacement | `informat.Misc.eval('${name}', {name:'test'})` |
| **safesql** | `sql: String, params: Array<Object>` | `String` | Generate safe complete SQL | `informat.Misc.safesql('select ?', ['test'])` |
| **uuid16** | No parameters | `String` | Generate 16-character UUID string | `informat.Misc.uuid16() // "lqjfw3xaglp38tru"` |
| **uuid32** | No parameters | `String` | Generate 32-character UUID string | `informat.Misc.uuid32() // "rigzv6usysisu2gmkash6hdg526y10b5"` |
| **newObject** | No parameters | `Object` | Create empty object | `informat.Misc.newObject() // {}` |
| **recordSql** | `sql: String, parameters: Array<Object>` | `Array<Object>` | Execute SQL to query data table records | `informat.Misc.recordSql('select * from table', [])` |

## String

String related functions. Call via `informat.String.method`

| Method | Parameters | Return Value | Description | Example |
|------|------|--------|------------------|------------|
| **upper** | `s: String` | `String` | Convert all letters to uppercase | `informat.String.upper('abc') // "ABC"` |
| **lower** | `s: String` | `String` | Convert all letters to lowercase | `informat.String.lower('ABC') // "abc"` |
| **concat** | `s1: String, s2: String` | `String` | Merge two strings | `informat.String.concat('a','b') // "ab"` |
| **lpad** | `s1: String, len: Integer, s2: String` | `String` | Pad characters at the beginning of string | `informat.String.lpad('ABC',6,'0') // "000ABC"` |
| **rpad** | `s1: String, len: Integer, s2: String` | `String` | Pad characters at the end of string | `informat.String.rpad('ABC',6,'0') // "ABC000"` |
| **trim** | `s: String` | `String` | Remove whitespace from both ends of string | `informat.String.trim(' abc ') // "abc"` |
| **replace** | `s: String, s1: String, s2: String` | `String` | Replace first occurrence of substring | `informat.String.replace('abca','a','_') // "_bca"` |
| **replaceAll** | `s: String, s1: String, s2: String` | `String` | Replace all occurrences of substring | `informat.String.replaceAll('abca','a','_') // "_bc_"` |
| **substr** | `s: String, start: Integer, len: Integer` | `String` | Extract substring from position with length | `informat.String.substr('abcd',1,2) // "bc"` |
| **substring** | `s: String, start: Integer, end: Integer` | `String` | Extract substring from start to end position | `informat.String.substring('abcd',0,2) // "ab"` |
| **indexOf** | `s: String, s2: String` | `Integer` | Get position of first occurrence of substring | `informat.String.indexOf('abcd','a') // 0` |
| **lastIndexOf** | `s: String, s2: String` | `Integer` | Get position of last occurrence of substring | `informat.String.lastIndexOf('abcad','a') // 3` |
| **contains** | `s: String, s2: String` | `Boolean` | Check if string contains substring | `informat.String.contains('abcd','a') // true` |
| **length** | `s: String` | `Integer` | Get string length | `informat.String.length('abcd') // 4` |
| **startsWith** | `s: String, s2: String` | `Boolean` | Check if string starts with substring | `informat.String.startsWith('abcd','a') // true` |
| **endsWith** | `s: String, s2: String` | `Boolean` | Check if string ends with substring | `informat.String.endsWith('abcd','d') // true` |
| **match** | `regex: String, input: String` | `Boolean` | Validate string with regular expression | `informat.String.match('^[a-z]+','abcd') // true` |
| **isEmpty** | `s: String` | `Boolean` | Check if string is empty (after trimming) | `informat.String.isEmpty(' ') // true` |
| **isNotEmpty** | `s: String` | `Boolean` | Check if string is not empty (after trimming) | `informat.String.isNotEmpty('a') // true` |
| **html2text** | `s: String` | `String` | Convert HTML content to text (XSS filtering) | `informat.String.html2text('<div>test</div>') // "test"` |

## User

User related operation functions in the current system. Call via `informat.User.method`

| Method | Parameters | Return Value | Description | Example |
|------|------|--------|------------------|------------|
| **usersWithRole** | `roleIdList: Array<String>` | `Array<String>` | Return users who have any of the specified roles | `informat.User.usersWithRole(['admin']) // [user1, user2, user3]` |
| **usersWithDepartment** | `departmentIdList: Array<String>` | `Array<String>` | Return users belonging to specified departments | `informat.User.usersWithDepartment(['yanfabu'])` |
| **superiorUsers** | `userId: String` | `Array<String>` | Return direct superiors of user | `informat.User.superiorUsers('user1') // [user2, user3]` |
| **superiorUsersWithLevel** | `userId: String, level: Integer` | `Array<String>` | Return consecutive superiors of user (specified levels) | `informat.User.superiorUsersWithLevel(Context.userId(), 1)` |
| **subordinateUsers** | `userId: String` | `Array<String>` | Return direct subordinates of user | `informat.User.subordinateUsers('user1') // [user2, user3]` |
| **subordinateUsersWithLevel** | `userId: String, level: Integer` | `Array<String>` | Return consecutive subordinates of user (specified levels) | `informat.User.subordinateUsersWithLevel('user1', 2) // [user2, user3]` |
| **leaderOfDept** | `departmentId: String` | `Array<String>` | Return leaders of a single department | `informat.User.leaderOfDept('dept1') // [user2, user3]` |
| **leaderOfDeptWithLevel** | `departmentId: String, level: Integer` | `Array<String>` | Return leaders of consecutive parent departments | `informat.User.leaderOfDeptWithLevel('yanfabu', 1)` |
| **leaderOfDeptList** | `departmentIdList: Array<String>` | `Array<String>` | Return leaders of multiple departments | `informat.User.leaderOfDeptList(['dept1', 'dept2']) // [user2, user3, user4]` |
| **parentOfDept** | `departmentId: String` | `String` | Return direct parent department ID | `informat.User.parentOfDept('dept1') // dept2` |
| **parentOfDeptList** | `departmentId: String` | `Array<String>` | Return all parent department IDs | `informat.User.parentOfDept('dept1') // ['dept2', 'dept3']` |
| **childrenOfDept** | `departmentId: String` | `Array<String>` | Return all sub-departments of a single department (recursive) | `informat.User.childrenOfDept('dept1') // [dept2, dept3]` |
| **childrenOfDeptList** | `departmentList: Array<String>` | `Array<String>` | Return all sub-departments of multiple departments | `informat.User.childrenOfDeptList(['dept1', 'dept2']) // [dept2, dept3]` |
| **directChildrenOfDept** | `departmentId: String` | `Array<String>` | Return direct sub-departments | `informat.User.directChildrenOfDept('dept1') // [dept2]` |
| **user** | `userId: String` | `User` | Return user information object | `informat.User.user(Context.userId())` |
| **userInfo** | `userId: String` | `UserInfo` | Return detailed user information object | `informat.User.userInfo(Context.userId())` |
| **deptList** | `departmentIdList: Array<String>` | `Array<Dept>` | Return department information object list | `informat.User.deptList(['dept1', 'dept2'])` |
| **dept** | `deptId: String` | `Dept` | Return department information object | `informat.User.dept('dept1')` |

## Context

Context related functions. Context represents environment parameters during execution. Call via `informat.Context.method`

| Method | Parameters | Return Value | Description | Example |
|------|------|--------|------------------|------------|
| **userId** | No parameters | `String` | Return current operating user ID | `informat.Context.userId() // "ek5veueb6c9zg"` |
| **appId** | No parameters | `String` | Return current application ID | `informat.Context.appId()` |
| **appEnvProp** | `propKey: String` | `String` | Return application environment variable value | `informat.Context.appEnvProp('payURL') // "http://dev-demo.com/pay"` |
| **httpHeaders** | No parameters | `Object` | Return current HTTP request header information | `informat.Context.httpHeaders() // {headers: {...}}` |
| **clipboardType** | No parameters | `String` | Return application clipboard data type | `informat.Context.clipboardType() // "test"` |
| **clipboardData** | No parameters | `Object` | Return application clipboard stored data | `informat.Context.clipboardData()` |
| **weworkAccessToken** | No parameters | `String` | Return WeCom AccessToken | `informat.Context.weworkAccessToken()` |
| **dingtalkAccessToken** | No parameters | `String` | Return DingTalk AccessToken | `informat.Context.dingtalkAccessToken()` |
| **feishuAccessToken** | No parameters | `String` | Return Feishu app AccessToken | `informat.Context.feishuAccessToken()` |
| **feishuTenantAccessToken** | No parameters | `String` | Return Feishu tenant AccessToken | `informat.Context.feishuTenantAccessToken()` |
| **requestIp** | No parameters | `String` | Return current request IP address | `informat.Context.requestIp() // "192.168.1.1"` |
| **hasAppPerm** | `permKey: String` | `Boolean` | Check if user has application permission | `informat.Context.hasAppPerm('admin') // true` |
| **hasModulePerm** | `moduleKey: String, permKey: String` | `Boolean` | Check if user has module permission | `informat.Context.hasModulePerm('crm', 'read') // true` |

## Record

Data table related functions. Call via `informat.Record.method`

| Method | Parameters | Return Value | Description | Example |
|------|------|--------|------------------|------------|
| **getById** | `tableId: String, recordId: String` | `Object` | Query data table record by ID | `informat.Record.getById('order', 'z2koxrkxtp854') // {amount:11, name:'测试采购单', id:'z2koxrkxtp854'}` |
| **getFieldValue** | `tableId: String, recordId: String, fieldId: String` | `Object` | Get field value of a data table record | `informat.Record.getFieldValue('order','z2koxrkxtp854','amount') // 11` |
| **getByField** | `tableId: String, fieldId: String, opt: String, value: Object` | `Array<Record>` | Filter records by single field | `informat.Record.getByField('order', 'amount', 'eq', 11) // [{amount:11, name:'测试采购单', id:'z2koxrkxtp854'}]` |
| **getByFields** | `tableId: String, conditions: Array` | `Array<Record>` | Filter records by multiple fields | `informat.Record.getByFields('tab', [{fieldId:'text', opt:'eq', value:'13'}]) // [{amount:11, text:'13', id:'z2koxrkxtp854'}]` |
| **getRecordOptionName** | `tableId: String, fieldId: String, value: String` | `String` | Return name of a single option value | `informat.Record.getRecordOptionName('order', 'type', 'a') // "Option 1"` |
| **getRecordOptionNames** | `tableId: String, fieldId: String, valueList: Array<String>, join: String` | `String` | Return names of multiple option values and join them | `informat.Record.getRecordOptionNames('order', 'type', ['a','b'], ',') // "Option 1,Option 2"` |
| **getRecordOptions** | `tableId: String, fieldId: String` | `Array<Option>` | Return option value list | `informat.Record.getRecordOptions('order', 'type') // [{id:'a',name:'Option 1'},{id:'b',name:'Option 2'}]` |
| **getRelationList** | `tableId: String, fieldId: String, recordId: String` | `Array<Record>` | Return values of a relation list field | `informat.Record.getRelationList('order','orderDetail','z2koxrkxtp854')` |

## T

Internationalization related functions. Call via `informat.T.method`

| Method | Parameters | Return Value | Description | Example |
|------|------|--------|------------------|------------|
| **locale** | No parameters | `String` | Get current language | `informat.T.locale() // "zh-CN"` |
| **t** | `key: String, args: Object/Array` | `String` | Translate by translation identifier and parameters | `informat.T.t('welcome.message') // "Welcome"` |
| **tWithLocale** | `locale: String, key: String, args: Object/Array` | `String` | Translate with specified language | `informat.T.tWithLocale('en-US', 'welcome.message') // "Welcome"` |
