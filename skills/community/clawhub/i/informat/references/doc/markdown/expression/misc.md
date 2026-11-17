# Misc

## Overview

Utility functions



## jsonStringify

Converts object obj to a JSON string

```javascript
Misc.jsonStringify(obj)
```

| Parameter | Type | Description |
|-----|--------|----------|
| obj | `Object` | Object to serialize |

**Return Value**

Type `String`
obj serialized as a JSON string, returns `null` if obj is `null`

**Example**

```javascript
Misc.jsonStringify('123456'); //"123456"
Misc.jsonStringify([1, 2, 3, 4, 5, 6]); //[1,2,3,4,5,6]
Misc.jsonStringify({ "a": 1, "b": 2 }); //{"a":1,"b":2}
Misc.jsonStringify(date); //1667232000000
Misc.jsonStringify(true); //true
Misc.jsonStringify(null); //null
```

## jsonStringifyPretty

Converts object obj to a formatted JSON string (pretty print)

```javascript
Misc.jsonStringifyPretty(obj)
```

| Parameter | Type | Description |
|-----|--------|----------|
| obj | `Object` | Object to serialize |

**Return Value**

Type `String`
obj serialized as a formatted JSON string, returns `null` if obj is `null`

**Example**

```javascript
Misc.jsonStringifyPretty({ "a": 1, "b": 2 }); 
// Returns:
// {
//   "a": 1,
//   "b": 2
// }
Misc.jsonStringifyPretty(null); //null
```



## jsonParse

Converts string str to a JSON object

```javascript
Misc.jsonParse(str)
```

| Parameter | Type | Description |
|-----|--------|-------------|
| str | `String` | String to convert to object |

**Return Value**

Type `Object`
The converted object. Throws an exception if str is `null` or not a valid JSON structure

**Example**

```javascript
Misc.jsonParse('"123456"'); //123456
Misc.jsonParse('[1,2,3,4,5,6]'); //[1,2,3,4,5,6]
Misc.jsonParse('{"a":1,"b":2}'); //{a:1,b:2}
Misc.jsonParse(1667232000000); //1667232000000
Misc.jsonParse('"2022-12-03T15:31:10.844Z"'); //Sat Dec 03 23:31:10 CST 2022
Misc.jsonParse(true); //true
Misc.jsonParse(null); //null
```



## parseFloat

Converts string str to a decimal number

```javascript
Misc.parseFloat(str)
```

| Parameter | Type | Description |
|-----|--------|----------|
| str | `String` | String to convert |

**Return Value**

Type `Double`
The converted decimal. Throws an exception if str is `null` or not a valid number format

**Example**

```javascript
Misc.parseFloat(1); //1.0
Misc.parseFloat(2.0); //2.0
Misc.parseFloat('2'); //2.0
Misc.parseFloat('a'); //null
Misc.parseFloat(true); //null
Misc.parseFloat(null); //null
```



## parseInt

Converts string str to an integer

```javascript
Misc.parseInt(str)
```

| Parameter | Type | Description |
|-----|--------|----------|
| str | `String` | String to convert |

**Return Value**

Type `Integer`
The converted integer. Throws an exception if str is `null` or not a valid number format

**Example**

```javascript
Misc.parseInt(1); //1
Misc.parseInt(2.0); //2
Misc.parseInt('2'); //2
Misc.parseInt('3.1415'); //3
Misc.parseInt('03.1415'); //3
Misc.parseInt('a'); //null
Misc.parseInt(true); //null
Misc.parseInt(null); //null
```



## timestampToDate

Converts a UNIX timestamp numeric value to a date type

```javascript
Misc.timestampToDate(timestamp)
```

| Parameter | Type | Description |
|-----------|---------|---------|
| timestamp | `Integer` | UNIX timestamp |

**Return Value**

Type `Date`
The converted date, returns `null` if timestamp is `null`

**Example**

```javascript
Misc.timestampToDate(1667232000000); //Tue Nov 01 00:00:00 CST 2022
Misc.timestampToDate('1667232000000'); //Tue Nov 01 00:00:00 CST 2022
Misc.timestampToDate('3.1415'); //null
Misc.timestampToDate('a'); //null
Misc.timestampToDate(null); //null
```



## dateToTimestamp

Converts a date type to a UNIX timestamp numeric value

```javascript
Misc.dateToTimestamp(date)
```

| Parameter | Type | Description |
|------|------|----|
| date | `Date` | Date |

**Return Value**

Type `Integer`
The converted UNIX timestamp, returns `null` if date is `null`

**Example**

```javascript
Misc.dateToTimestamp(new Date()); //1667232000000
Misc.timestampToDate(null); //null
```



## formatDate

Converts the variable date to a string according to format fmt (yyyy-MM-dd HH:mm:ss,SSS)

```javascript
Misc.formatDate(date, fmt)
```

| Parameter | Type | Description |
|------|--------|--------|
| date | `Date`   | Date to convert |
| fmt  | `String` | Format |

**Return Value**

Type `String`
The converted string, returns null if str is `null` or str is not in the given date format

**Example**

```javascript
//Assuming date value is 2022-11-01 13:01:01,000, timestamp is 1667278861000
Misc.formatDate(date, 'yyyy-MM'); //2022-11
Misc.formatDate(date, 'yyyy-MM-dd'); //2022-11-01
Misc.formatDate(date, 'yyyy'); //2022
Misc.formatDate(date, 'HH:mm:ss,SSS'); //13:01:01,000
Misc.formatDate(date, 'abc'); //null
Misc.formatDate(timestamp, 'yyyy-MM'); //2022-11
Misc.formatDate(timestamp, 'yyyy-MM-dd'); //2022-11-01
Misc.formatDate(timestamp, 'yyyy'); //2022
Misc.formatDate(timestamp, 'HH:mm:ss,SSS'); //13:01:01,000
Misc.formatDate(timestamp, 'abc'); //null
Misc.formatDate(null, 'yyyy-MM-dd'); //null
Misc.formatDate(date, null); //null
Misc.formatDate(timestamp, null); //null
Misc.formatDate(null, null); //null
```



## parseDate

Converts str to a date according to format fmt (yyyy-MM-dd HH:mm:ss,SSS)

```javascript
Misc.parseDate(str, fmt)
```

| Parameter | Type | Description |
|-----|--------|-----------|
| str | `String` | Date string to convert |
| fmt | `String` | Format |

**Return Value**

Type `Date`
The converted date, returns null if str is `null` or str is not in the given date format

**Example**

```javascript
Misc.parseDate('2022-11-01 13:01:01,000', 'yyyy-MM'); //Tue Nov 01 00:00:00 CST 2022
Misc.parseDate('2022-11-01 13:01:01,000', 'yyyy-MM-dd'); //Tue Nov 01 00:00:00 CST 2022
Misc.parseDate('2022-11-01 13:01:01,000', 'yyyy'); //Sat Jan 01 00:00:00 CST 2022
Misc.parseDate('2022-11-01 13:01:01,000', 'HH:mm:ss,SSS'); //null
Misc.parseDate('2022-11-01 13:01:01,000', 'abc'); //null
Misc.parseDate(null, 'yyyy-MM-dd'); //null
Misc.parseDate('2022-11-01 13:01:01,000', null); //null
Misc.parseDate(null, null); //null
```



## host

Returns the system's home page URL

```javascript
Misc.host()
```

**Return Value**

Type `String`
The system's home page URL

**Example**

```javascript
Misc.host() // https://next.informat.cn/ 
```

## intranetHost

Returns the system's intranet URL

```javascript
Misc.intranetHost()
```

**Return Value**

Type `String`
The system's intranet URL

**Example**

```javascript
Misc.intranetHost() // https://next-internal.informat.cn/
```



## pinyin

Returns the Chinese pinyin of string str

```javascript
Misc.pinyin(str)
```

| Parameter | Type | Description |
|-----|--------|------------|
| str | `String` | String to convert to pinyin |

**Return Value**

Type `String`
The converted pinyin, returns `null` if str is `null`

**Example**

```javascript
Misc.pinyin('你好织信'); //ni hao zhi xin
Misc.pinyin('Hellow 织信'); //H e l l o w   zhi xin
Misc.pinyin(null); //null
```



## shortPinyin

Returns the first letter of pinyin for each Chinese character in string str

```javascript
Misc.shortPinyin(str)
```

| Parameter | Type | Description |
|-----|--------|------------|
| str | `String` | String to convert to pinyin |

**Return Value**

Type `String`
The converted pinyin initials, returns `null` if str is `null`

**Example**

```javascript
Misc.shortPinyin('你好织信'); //nhzx
Misc.shortPinyin('Hellow 织信'); //Hellow zx
Misc.shortPinyin(null); //null
```



## expectNotNull

Determines whether an object is null. If null, throws an exception with message as the prompt; otherwise returns the object

```javascript
Misc.expectNotNull(obj, message)
```

| Parameter | Type | Description |
|---------|--------|-----------------|
| obj     | `Object` | Object to check |
| message | `String` | Exception message if obj is null |

**Return Value**

Type `Object`
The passed-in object

**Example**

```javascript
Misc.expectNotNull(null, '消息') //throws exception
Misc.expectNotNull('obj', '消息') //returns 'obj'
```



## expectFirst

Returns the first element of array. If array is empty, throws an exception with message as the prompt

```javascript
Misc.expectFirst(array, message)
```

| Parameter | Type | Description |
|---------|--------|----------------------------|
| array   | `Array`  | Array |
| message | `String` | Exception message if array is null or has length 0 |

**Return Value**

Type `Object`
The first element of array

**Example**

```javascript
Misc.expectFirst(null, '消息') //throws exception
Misc.expectFirst([], '消息') //throws exception
Misc.expectFirst(['1', '2'], '消息') //returns 1
```



## expectLast

Returns the last element of array. If array is empty, throws an exception with message as the prompt

```javascript
Misc.expectLast(array, message)
```

| Parameter | Type | Description |
|---------|--------|----------------------------|
| array   | `Array`  | Array |
| message | `String` | Exception message if array is null or has length 0 |

**Return Value**

Type `Object`
The last element of array

**Example**

```javascript
Misc.expectLast(null, '消息') //throws exception
Misc.expectLast([], '消息') //throws exception
Misc.expectLast(['1', '2'], '消息') //returns 2
```

## log

Logs information

```javascript
Misc.log(obj)
```

| Parameter | Type | Description |
|-----|--------|----------|
| obj | `Object` | Object to log |

**Return Value**

Type `Boolean` Always returns `true`

**Example**

```javascript
Misc.log("debug info") // logs, returns true
Misc.log({name: "test", value: 123}) // logs object
```



## invokeScript

Calls a function in a script

Functions in the script must be exported using `export` syntax. Throws an exception if the script or function does not exist

```javascript
Misc.invokeScript(script, func, ...args)
```

| Parameter | Type | Description |
|--------|-----------|-------|
| script | `String`    | Script path |
| func   | `String`    | Function name |
| args   | `...Object` | Parameter list |

**Return Value**

Type `Object`
The return value of the script function, `null` if the function has no return value

**Example**

Script test.js
```javascript
export function add(a, b) {
    return a + b;
}
```

```javascript
Misc.invokeScript('test.js', 'add1') //throws exception
Misc.invokeScript('test.js', 'add', 1, 2) //3
```



## invokeAutomatic

Calls an automation program

Throws an exception if the automation program does not exist

```javascript
Misc.invokeAutomatic(automaticId, ...args)
```

| Parameter | Type | Description |
|-------------|-----------|-----------|
| automaticId | `String`    | Automation program identifier |
| args        | `...Object` | Parameter list |

**Return Value**

Type `Object`
The return value of the automation program, `null` if the automation program has no return value

**Example**

```javascript
Misc.invokeAutomatic('testAutomatic', 1, 2) //3
```

## invokeLibrary

Calls a library function

```javascript
Misc.invokeLibrary(key, className, methodName, parameters)
```

| Parameter | Type | Description |
|-------------|-----------------|-----------|
| key         | `String`        | Library identifier |
| className   | `String`        | Class name |
| methodName  | `String`        | Method name |
| parameters  | `Array<Object>` | Parameter list |

**Return Value**

Type `Object`
The return value of the library function

**Example**

```javascript
Misc.invokeLibrary('demo', 'DemoClass', 'hello', ['world'])
```



## httpGet

Accesses a URL via GET method and returns the response content

Throws an exception if the URL is invalid or if the HTTP response code is not 200

```javascript
Misc.httpGet(url)
```

| Parameter | Type | Description |
|-----|--------|-------|
| url | `String` | URL address |

**Return Value**

Type `String`
The body content returned by the HTTP request

**Example**

```javascript
Misc.httpGet('https://next.informat.cn/web0/api/i1mwqy35y88hl/helloworld') //hello world!
```



## prop

Gets the value of property key from object

If the object is a `Map` type, returns the item with key `key`. If it is an object type, returns its `key` property. Returns null if object is `null`

```javascript
Misc.prop(object, key)
```

| Parameter | Type | Description |
|--------|--------|------------------------|
| object | `Object` | Object to get property from |
| key    | `String` | Name of the property to return, throws exception if key is empty |

**Return Value**

Type `Object`
The value of property key in object

**Example**
Assuming object structure is as follows:

```javascript
Misc.prop({ 'a': '1', 'b': 2 }, 'a'); //1
Misc.prop({ 'a': '1', 'b': 2 }, 'c'); //null
Misc.prop({ 'a': '1', 'b': 2 }, null); //null
Misc.prop(null, 'c'); //null
Misc.prop(null, null); //null
```

## props

Gets a new object containing the properties from the props list of object

```javascript
Misc.props(object, props)
```

| Parameter | Type | Description |
|--------|-----------------|--------------------------------|
| object | `Object`        | Object to get properties from |
| props  | `Array<String>` | New object with properties from the list, throws exception if props is null |

**Return Value**

Type `Object`
The value of properties in object

**Example**
Assuming object structure is as follows:

```javascript
Misc.props({ 'a': '1', 'b': 2 }, 'a'); // {'a':'1'}
Misc.props({ 'a': '1', 'b': 2 }, 'a', 'b'); // {'a':'1','b':2}
Misc.props({ 'a': '1', 'b': 2 }, ['a', 'b']); // {'a':'1','b':2}
Misc.props({ 'a': '1', 'b': 2 }, null); //{}
Misc.props(null, 'c'); //null
Misc.props(null, null); //exception
```

## transform

Returns a new object composed by mapping the element according to the mapping

```javascript
Misc.transform(object, mapping);
```

| Parameter | Type | Description |
|---------|----------------------|---------|
| list    | `Array`              | Collection 1 |
| mapping | `Map<String,String>` | Property mapping object |

**Return Value**


Returns a new object composed by mapping the element according to the mapping

**Example**

```javascript
Misc.transform({ 'name': '张三', 'age': 1 }, { 'name': 'userName', 'age': 'userAge' }); //{'userName':'张三','userAge':1}
Misc.transform({ 'name': '张三', 'age': 1 }, { 'name': 'userName', 'sex': 'userSex' }); //{'userName':'张三','userSex':null}
Misc.transform({ 'name': '张三', 'age': 1 }, null); // {}
Misc.transform(null, { 'name': 'userName', 'age': 'userAge' }); // null
Misc.transform(null, null); // null
```

## appId

Gets the ID of the current application

```javascript
Misc.appId()
```

**Return Value**

Type `String`
The ID of the current application



## getAppIdByKey

Queries the application ID within the team by application identifier

```javascript
Misc.getAppIdByKey(key)
```

| Parameter | Type | Description |
|-----|--------|-------|
| key | `String` | Application identifier |

#### Return Value

Type `String`
Application ID



## attachmentURL

Gets the access URL for an attachment

Gets the access URL through the data table identifier, field identifier, and value of an attachment field

```javascript
Misc.attachmentURL(tableKey, fieldKey, value)
```

| Parameter | Type | Description |
|----------|--------|-----------------------|
| tableKey | `String` | Data table ID |
| fieldKey | `String` | Field ID |
| value    | `String` | The id property in TableAttachment |

**Return Value**
Type `String`
The access URL of the attachment

**Example**

```javascript
Misc.attachmentURL('staff', 'photo', '1af34d8a031d4faeaef40a989585caa5.png')
//https://next.informat.cn/web0/file/fieldkey/psl4wawpyued1/staff/photo/1af34d8a031d4faeaef40a989585caa5.png
```



## appResURL

Gets the resource URL from the application resource library

Gets the access URL by passing the resource library resource ID

```javascript
Misc.appResURL(appResId)
```

| Parameter | Type | Description |
|----------|--------|-----------------------|
| appResId | `String` | Resource ID |

**Return Value**
Type `String`
The resource access URL from the resource library

**Example**

```javascript
Misc.appResURL('cjkhd8819chd8dhs.jpg')
//https://next.informat.cn/web0/main/app_res/icxt9rsd1f0ai/demoApp/cjkhd8819chd8dhs.jpg
```



## websiteResURL

Gets the resource URL of an application website module

Gets the access URL by passing the website module ID and resource path

```javascript
Misc.websiteResURL(moduleKey,filePath)
```

| Parameter | Type | Description |
|-----------|--------|--------|
| moduleKey | `String` | Website module ID |
| filePath  | `String` | File path |

**Return Value**
Type `String`
The resource URL of the website module

**Example**

```javascript
Misc.websiteResURL('websiteModule', 'logo.png');
//https://next.informat.cn/web0/website/od6km3qte7vdb/j8j56sgtoj8b7/logo.png
Misc.websiteResURL('websiteModule', './logo.png');
//https://next.informat.cn/web0/website/od6km3qte7vdb/j8j56sgtoj8b7/./logo.png
```



## barcodeURL

Returns the BASE64 value of a barcode image

```javascript
Misc.barcodeURL(value, format)
```

| Parameter | Type | Description |
|--------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| value  | `String` | Barcode value, can only contain numbers |
| format | `String` | Barcode format, options are `CODE39` `CODE128` `CODE128A` `CODE128B` `CODE128C` `ISBN` `EAN13` `EAN8` `EAN5` `EAN2` `UPC` `ITF` `ITF14` `MSI` `MSI11` `MSI1010` `MSI1110` `pharmacode` `codabar` |

**Return Value**
Type `String`
BASE64 value of the barcode image

**Example**

```javascript
Misc.barcodeURL('12345', 'CODE39');
// data:image/png;base64,...
```



## qrcodeURL

Returns the BASE64 value of a QR code image

```javascript
Misc.qrcodeURL(value, format)
```

| Parameter | Type | Description |
|--------|----------|----------|
| value  | `String`   | QR code content |
| width | `Interger` | Size of the generated QR code |

**Return Value**
Type `String`
BASE64 value of the QR code image

**Example**

```javascript
Misc.qrcodeURL('12345', 300)
// data:image/jpeg;base64,...
```



## eval

Uses context variables to execute the expression engine and replace data in the expression string str template

```javascript
Misc.eval(str, context)
```

| Parameter | Type | Description |
|---------|--------|--------|
| str     | `String` | Expression string |
| context | `Object` | Context variables |

**Return Value**
Type `Object`
The value after template expression execution

**Example**

```javascript
Misc.eval(null,null) // null
Misc.eval('${true}',null)// true
Misc.eval('${true}',{}) // true
Misc.eval('name',{"name":"informat"}) // 'name'
Misc.eval('${name}',{"name":"informat"}) // 'informat'
Misc.eval('${detail.age}',{"name":"informat","detail":{"age":12}}) // 12
Misc.eval('${detail.sex}',{"name":"informat","detail":{"age":12}}) // null
Misc.eval(null,{"name":"informat"})//null
```

## safesql
Generates a safe complete SQL from a SQL with `?` placeholders
```javascript
Misc.safesql(sql, params);
```

| Parameter | Type | Description |
|---------|-----------------|--------|
| sql     | `String`        | SQL with `?` placeholders |
| params | `Array<Object>` | Parameters, replaced in order corresponding to placeholder positions |

**Return Value**

Type `String`
Safe SQL

**Example**

```javascript
Misc.safesql(`update tab set age=?,name=? where id=?`, [18, "李四", `'张' or 1=1`]) 
// update tab set age=18,name='李四' where id='''张'' or 1=1'
```

## uuid16
Generates a 16-character UUID string
```javascript
Misc.uuid16();
```

**Return Value**

Type `String`

**Example**

```javascript
Misc.uuid16()//lqjfw3xaglp38tru
Misc.uuid16()//xnqdnq24zubdrk1y
```

## uuid32
Generates a 32-character UUID string
```javascript
Misc.uuid32();
```

**Return Value**

Type `String`

**Example**

```javascript
Misc.uuid32()//rigzv6usysisu2gmkash6hdg526y10b5
Misc.uuid32()//h7b1gde1bz402kwhgoq383hfl6k2p77m
```

## newObject
Constructs an empty object
```javascript
Misc.newObject();
```

**Return Value**

Type `Object`

**Example**

```javascript
Misc.newObject()//{}
```


## recordSql

Executes a SQL query on data table records. Only `Select` statements are allowed, and only records from data table modules are supported.

```javascript
Misc.recordSql(sql, parameters)
```

| Parameter | Type | Description |
|----------|--------|-----------------------|
| sql | `String` | SQL statement |
| parameters | `Array<Object>` | Parameter list |

**Return Value**

Type `Array<Object>`
Query result set

**Example**

:::: tabs
::: tab Call
```javascript
Misc.recordSql('select id,name from task where status=? ',['1']);
```
::: 
::: tab Return
```json
[
  {
    "name": "名称",
    "id": "pht21vzu5ozps"
  },
  {
    "name": "333",
    "id": "1"
  }
]
```
:::
::::
