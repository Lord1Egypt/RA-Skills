# Encode

## Overview

String encoding and decoding related functions

## md5

Returns the MD5 hash of string s

```javascript
Encode.md5(s)
```

| Parameter | Type | Description |
|----|--------|----------|
| s  | `String` | String to compute |

**Return Value**

Type `String`
The `md5` hash value of string s

**Example**

```javascript
Encode.md5('123456'); //e10adc3949ba59abbe56e057f20f883e
Encode.md5(null); //null
```



## urlEncode

URL-encodes string str

```javascript
Encode.urlEncode(str)
```

| Parameter | Type | Description |
|-----|--------|----------|
| str | `String` | String to encode |

**Return Value**

Type `String`
The URL-encoded value of string str

**Example**

```javascript
Encode.urlEncode('https://next.informat.cn'); //https%3A%2F%2Fnext.informat.cn
Encode.urlEncode(null); //null
```



## urlDecode

URL-decodes string str

```javascript
Encode.urlDecode(str)
```

| Parameter | Type | Description |
|-----|--------|----------|
| str | `String` | String to decode |

**Return Value**

Type `String`
The URL-decoded value of string str

**Example**

```javascript
Encode.urlDecode('https%3A%2F%2Fnext.informat.cn'); //https://next.informat.cn
Encode.urlDecode(null); //null
```

## escape

Escapes special characters in a string

```javascript
Encode.escape(str)
```

| Parameter | Type | Description |
|-----|----------|----------|
| str | `String` | String to escape |

**Return Value**

Type `String`
The escaped string

**Example**

```javascript
Encode.escape('"hello" & "world"') // "&quot;hello&quot; &amp; &quot;world&quot;"
Encode.escape(null) // null
```

## unescape

Restores an escaped string to its original form

```javascript
Encode.unescape(str)
```

| Parameter | Type | Description |
|-----|----------|----------|
| str | `String` | String to restore |

**Return Value**

Type `String`
The restored string

**Example**

```javascript
Encode.unescape('&quot;hello&quot; &amp; &quot;world&quot;') // '"hello" & "world"'
Encode.unescape(null) // null
```
