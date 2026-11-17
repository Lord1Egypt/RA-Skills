# String

## Overview

String related functions

## upper

Converts all letters in the string to uppercase

```javascript
String.upper(s)
```

| Parameter | Type | Description |
|----|--------|----------|
| s  | `String` | String to convert |

**Return Value**

Type `String`
Uppercase string, returns null if s is empty

**Example**

```javascript
String.upper(1); //1
String.upper('Informat织信'); //INFORMAT织信
String.upper('abc'); //ABC
String.upper('aBC'); //ABC
String.upper(null); //null
```

## lower

Converts all letters in the string to lowercase

```javascript
String.lower(s)
```

| Parameter | Type | Description |
|----|--------|----------|
| s  | `String` | String to convert |

**Return Value**

Type `String`
Converted lowercase string, returns null if s is empty

**Example**

```javascript
String.lower(1); //1
String.lower('Informat织信'); //informat织信
String.lower('ABC'); //abc
String.lower('aBC'); //abc
String.lower(null); //null
```

## concat

Merges multiple objects into a single string

```javascript
String.concat(s1, s2, s3 ...)
```

| Parameter | Type | Description |
|----|--------|---------|
| s1 | `String` | Object to concatenate |
| s2 | `String` | Object to concatenate |

**Return Value**

Type `String`
Concatenated string

**Example**

```javascript
String.concat('Informat', '织信'); //Informat织信
String.concat('Informat', 1, '2'); //Informat1
String.concat('Informat', true); //Informattrue
String.concat('Informat', null); //Informat
String.concat(null, '织信'); //织信
String.concat(null, null); //null
```

## lpad

Pads string s2 at the beginning of string s1 until the string reaches length len

```javascript
String.lpad(s1, len, s2)
```

| Parameter | Type | Description |
|-----|---------|---------|
| s1  | `String`  | String to pad |
| s2  | `String`  | Padding character |
| len | `Integer` | Total length |

**Return Value**

Type `String`
Padded string

**Example**

```javascript
String.lpad(1, 3, 0); //001
String.lpad('ABC', 6, 0); //000ABC
String.lpad('ABC', 6, '_'); //___ABC
String.lpad('ABC', 6, null); //ABC
String.lpad('ABC', 2, '0'); //ABC
String.lpad('ABC', null, 0); //ABC
String.lpad(null, 2, null); //null
String.lpad(null, null, null); //null
```

## rpad

Pads string s2 at the end of string s1 until the string reaches length len

```javascript
String.rpad(s1, len, s2)
```

| Parameter | Type | Description |
|-----|---------|---------|
| s1  | `String`  | String to pad |
| s2  | `String`  | Padding character |
| len | `Integer` | Total length |

**Return Value**

Type `String`
Padded string

**Example**

```javascript
String.rpad(1, 3, 0); //100
String.rpad('ABC', 6, 0); //ABC000
String.rpad('ABC', 6, '_'); //ABC___
String.rpad('ABC', 6, null); //ABC
String.rpad('ABC', 2, '0'); //ABC
String.rpad('ABC', null, 0); //ABC
String.rpad(null, 2, null); //null
String.rpad(null, null, null); //null
```

## trim

Removes all whitespace characters from both sides of string s

```javascript
String.trim(s)
```

| Parameter | Type | Description |
|----|--------|---------|
| s  | `String` | String to process |

**Return Value**

Type `String`
String with whitespace removed

**Example**

```javascript
String.trim(' abc '); //abc
String.trim(''); //
String.trim(null); //null
```

## replace

Replaces the first occurrence of string s1 in string s with string s2

```javascript
String.replace(s, s1, s2)
```

| Parameter | Type | Description |
|----|--------|---------|
| s  | `String` | String to process |
| s1 | `String` | Substring to replace |
| s2 | `String` | Replacement string |

**Return Value**

Type `String`
String with content replaced

**Example**

```javascript
String.replace('abca', 'a', '_'); //_bca
String.replace('abca', 'a', ''); //bca
String.replace('abca', 'a', null); //abca
String.replace('abca', null, '_'); //abca
String.replace(null, 'a', '_'); //null
String.replace(null, null, '_'); //null
String.replace(null, null, null); //null
```

## replaceAll

Replaces all occurrences of string s1 in string s with string s2

```javascript
String.replaceAll(s, s1, s2)
```

| Parameter | Type | Description |
|----|--------|---------|
| s  | `String` | String to process |
| s1 | `String` | Substring to replace |
| s2 | `String` | Replacement string |

**Return Value**

Type `String`
String with content replaced

**Example**

```javascript
String.replaceAll('abca', 'a', '_'); //_bc_
String.replaceAll('abca', 'a', ''); //bc
String.replaceAll('abca', 'a', null); //abca
String.replaceAll('abca', null, '_'); //abca
String.replaceAll(null, 'a', '_'); //null
String.replaceAll(null, null, '_'); //null
String.replaceAll(null, null, null); //null
```



## substr

Extracts len characters from string s starting at index position start

```js
String.substr(s,start,len)
```

| Parameter | Type | Description |
|-------|---------|--------------------------|
| s     | `String`  | String to process |
| start | `Integer` | Start position. Index starts from 0. Defaults to 0 if null |
| len   | `Integer` | Length to extract. Defaults to 0 if null |

**Return Value**

Type `String`
Extracted string

**Example**

```javascript
String.substr('abcd', 1, 2); //bc
String.substr('abcd', 1, 5); //bcd
String.substr('abcd', -1, 5); //abcd
String.substr('abcd', null, 5); //abcd
String.substr('abcd', 1, null); //
String.substr(null, null, 5); //null
```



## substring

Extracts from string s from start position to end position

```js
String.substring(s,start,end)
```

| Parameter | Type | Description |
|-------|---------|--------------------------|
| s     | `String`  | String to process |
| start | `Integer` | Start position. Index starts from 0. Defaults to 0 if null |
| end   | `Integer` | End position. Index starts from 0. Defaults to 0 if null |

**Return Value**

Type `String`
Extracted string

**Example**

```javascript
String.substring('abcd', 0, 2); //ab
String.substring('abcd', 0, 5); //abcd
String.substring('abcd', -1, 5); //abcd
String.substring('abcd', 2, 3); //c
String.substring('abcd', null, 5); //abcd
String.substring('abcd', 1, null); //
String.substring(null, null, 5); //null
```



## indexOf

Gets the position of the first occurrence of string s2 in string s

```js
String.indexOf(s,s2)
```

| Parameter | Type | Description |
|----|--------|--------|
| s  | `String` | String to search |
| s2 | `String` | String s2 |

**Return Value**

Type `Integer`
Position of first occurrence. Returns 0-based index position if s2 exists in s, otherwise returns -1

**Example**

```javascript
String.indexOf('abcd', 'a'); //0
String.indexOf('abcad', 'a'); //0
String.indexOf('abcd', 'cd'); //2
String.indexOf('abcd', 'g'); //-1
String.indexOf('abcd', null); //-1
String.indexOf(null, 'a'); //-1
String.indexOf(null, null); //-1
```



## lastIndexOf

Gets the position of the last occurrence of string s2 in string s

```js
String.lastIndexOf(s,s2)
```

| Parameter | Type | Description |
|----|--------|--------|
| s  | `String` | String to search |
| s2 | `String` | String s2 |

**Return Value**

Type `Integer`
Position of last occurrence. Returns 0-based index position if s2 exists in s, otherwise returns -1

**Example**

```javascript
String.lastIndexOf('abcd', 'a'); //0
String.lastIndexOf('abcad', 'a'); //3
String.lastIndexOf('abcd', 'cd'); //2
String.lastIndexOf('abcd', 'g'); //-1
String.lastIndexOf('abcd', null); //-1
String.lastIndexOf(null, 'a'); //-1
String.lastIndexOf(null, null); //-1
```



## contains

Determines whether string s contains string s2

```js
String.contains(s,s2)
```

| Parameter | Type | Description |
|----|--------|--------|
| s  | `String` | String to search |
| s2 | `String` | String s2 |

**Return Value**

Type `Boolean`
Whether it contains

**Example**

```javascript
String.contains('abcd', 'a'); //true
String.contains('abcad', 'a'); //true
String.contains('abcd', 'cd'); //true
String.contains('abcd', 'g'); //false
String.contains('abcd', null); //false
String.contains(null, 'a'); //false
String.contains(null, null); //false
```



## length

Gets the length of string s

```js
String.length(s)
```

| Parameter | Type | Description |
|-----|--------|--------|
| s   | `String` | String to query |

**Return Value**

Type `Integer`
String length

**Example**

```javascript
String.length('abcd'); //4
String.length('abcd中文'); //6
String.length(null); //0
```



## startsWith

Determines whether string s starts with string s2

```js
String.startsWith(s, s2)
```

| Parameter | Type | Description |
|----|--------|--------|
| s  | `String` | String to search |
| s2 | `String` | String s2 |

**Return Value**

Type `Boolean`

**Example**

```javascript
String.startsWith('abcd', 'a'); //true
String.startsWith('abcad', 'bc'); //false
String.startsWith('abcad', 'g'); //false
String.startsWith('abcad', ''); //true
String.startsWith('', ''); //true
String.startsWith(null, 'a'); //false
String.startsWith(null, null); //false
```



## endsWith

Determines whether string s ends with string s2

```js
String.endsWith(s,s2)
```

| Parameter | Type | Description |
|----|--------|--------|
| s  | `String` | String to search |
| s2 | `String` | String s2 |

**Return Value**

Type `Boolean`

**Example**

```javascript
String.endsWith('abcd', 'a'); //false
String.endsWith('abcad', 'bc'); //false
String.endsWith('abcad', 'g'); //false
String.endsWith('abcad', ''); //true
String.endsWith('', ''); //true
String.endsWith(null, 'a'); //false
String.endsWith(null, null); //false
```



## match

Uses regular expression regex to validate whether input meets the requirements

```js
String.match(regex,input)
```

| Parameter | Type | Description |
|-------|--------|--------------------------|
| regex | `String` | Regex content. Does not currently support regex shorthands starting with `\` such as `\w`, `\d` |
| input | `String` | Content to match |

**Return Value**

Type `Boolean`

**Example**

```javascript
String.match('^[a-z]+', 'abcd'); //true
String.match('[^a-z]+', 'abcd'); //false
String.match('[^a-z][a-zA-Z0-9]*', '123abcd'); //true
String.match('^[a-z]+', 'abcd123'); //false
String.match('^[a-z]*', 'abc123'); //false
String.match('^a[a-zA-Z0-9]*', 'abc123'); //true
String.match('[a-zA-Z0-9]*[0-9]$', 'abc123'); //true
String.match('^"[a-zA-Z0-9]*', '"abc123'); //true
String.match(null, 'a'); //false
String.match(null, null); //false
```



## isEmpty

Determines whether input string s is empty

```js
String.isEmpty(s)
```

| Parameter | Type | Description |
|----|--------|---------------------|
| s  | `String` | Input content. The system will automatically trim leading and trailing spaces |

**Return Value**

Type `Boolean`

**Example**

```javascript
String.isEmpty(' a '); //false
String.isEmpty(''); //true
String.isEmpty(' '); //true
String.isEmpty(null); //true
```
## isNotEmpty

Determines whether input string s is not empty

```js
String.isNotEmpty(s)
```

| Parameter | Type | Description |
|----|--------|---------------------|
| s  | `String` | Input content. The system will automatically trim leading and trailing spaces |

**Return Value**

Type `Boolean`

**Example**

```javascript
String.isNotEmpty(' a '); //true
String.isNotEmpty(''); //false
String.isNotEmpty(' '); //false
String.isNotEmpty(null); //false
```

## html2text

Converts HTML content in string s to text content. This process uses an XSS filter to filter the content before output.

```js
String.html2text(s)
```

| Parameter | Type | Description |
|----|--------|------|
| s  | `String` | Input content |

**Return Value**

Type `String`

**Example**

```javascript
String.html2text("<div>示例数据，<strong>织信</strong>，<a href='https://www.informat.cn'>点击查看</a></div>"); //示例数据，织信，点击查看
String.html2text("<div>示例数据，<script>alert('织信')</script>，<a href='https://www.informat.com'>点击查看</a></div>"); //示例数据，<script>alert('织信')</script>，点击查看
String.html2text(''); //''
String.html2text(' '); //' '
String.html2text(null); //null
```
