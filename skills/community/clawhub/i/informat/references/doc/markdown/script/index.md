# Server-Side Scripts

## Overview

Informat uses `javascript` as its scripting language. Scripts in Informat can implement advanced features that cannot be achieved through configuration. In scripts, you can access system-provided utility functions through the `informat` object. Scripts run on the server side, and runtime state is isolated per application. For complex application scenarios, scripts offer greater flexibility than `automation` programs and also deliver better performance. Scripts are recommended for API or complex computation scenarios.

::: warning Terminating Script Execution
If a script takes too long to execute or its logic produces an infinite loop, you can terminate the script through the application [Runtime Status](/guide/app/run_log.md#终止当前任务) monitoring feature.
:::

## Modularization

Informat supports `javascript` `ES6` syntax. `Promise`, `setTimeout`, and other asynchronous operations are not supported. All function calls are synchronous. Note that although Informat's script engine is similar in usage to `nodejs`, they are completely different implementations. Browser objects like `window` and `document` cannot be used in Informat either -- **Informat scripts run on the server side**.

For large projects, it is recommended to organize script files into folders by functionality. Scripts can use `import` and `export` syntax for importing and exporting. The following example demonstrates this usage:

::::tabs
:::tab export-func.js

```javascript
export function add(a, b) {
    return a + b;
}
```

:::tab import-func.js

```javascript
import { add } from 'export-func.js'

const result = add(1, 2);

```

:::
::::

## npm Package Management

In Informat, you can use the npm package manager to load packages from the `npmjs.com` repository. Using `npm` can greatly extend the capabilities of scripts. In addition to using high-quality community-developed code, developers can also package their own common scripts as `npm` packages and publish them to the repository for use across multiple applications.
Libraries imported via `npm` packages need to use the `require` syntax. Here is an example:
1. Enable NPM configuration in the enterprise admin console
::: info Enable NPM Configuration in Enterprise Admin Console
Configuration path: System Information => Parameter Settings

![npmSetting.png](images/npmSetting.png)

[Configuration Details](../../guide/admin/setting#参数说明-8)
:::

2. Create a package.json file in the script root directory to manage dependent packages

```json
{
  "dependencies": {
    "crypto-js": "4.1.1"
  }
}
```

3. Use the require method to import packages in scripts

:::: tabs
::: tab Script
```js
	let SHA256 = require("crypto-js/sha256");
	console.log(SHA256("Message"));
```
:::

::: tab Output
```json
{
  "words": [
    796354186,
    -1644431147,
    -2071224597,
    1248937418,
    -1798902382,
    920954739,
    -153309275,
    321597329
  ],
  "sigBytes": 32
}
```
:::
::::


Informat's support for `npm` packages is not yet fully mature at this stage. If a package references `nodejs` built-in libraries such as `fs`, `events`, etc., these packages will not work properly. Additionally, `npm` packages do not support importing with the `import` syntax.

## Using Java Objects

Scripts can use Java objects. The following documentation shows you how to achieve interoperability with Java and possible JavaScript-to-Java embedding scenarios.


### Class Access
To access Java classes, the script engine supports the `Java.type(typeName)` function:

```js
var FileClass = Java.type('java.io.File');
```
By default, Java classes are not automatically mapped to global variables. For example, there is no global property for java in the script engine. Existing access code like java.io.File should be rewritten to use the `Java.type(name)` function:

```js
//Script engine compliant syntax
var FileClass = Java.type("java.io.File");
```


### Constructing Java Objects
Java objects can be constructed using JavaScript's `new` keyword:

```js
var FileClass = Java.type('java.io.File');
var file = new FileClass("myFile.md");
```

### Field and Method Access
Static fields of Java classes or fields of Java objects can be accessed like JavaScript properties:

```js
var JavaPI = Java.type('java.lang.Math').PI;
```

Java methods can be called like JavaScript functions:

```js
var file = new (Java.type('java.io.File'))("test.md");
var fileName = file.getName();
```

### Method Parameter Conversion
JavaScript is defined to operate on the `double` number type. For performance reasons (e.g., type `int`), the script engine may internally use other Java data types.

When calling Java methods, value conversion may be needed. This occurs when a Java method requires a `long` parameter and an `int` is provided by the script engine. If this conversion results in a lossy conversion, a `TypeError` will be thrown:

```java
//Java
void longArg   (long arg1);
void doubleArg (double arg2);
void intArg    (int arg3);
```

```js
//JavaScript
javaObject.longArg(1);     //widening, OK
javaObject.doubleArg(1);   //widening, OK
javaObject.intArg(1);      //match, OK

javaObject.longArg(1.1);   //lossy conversion, TypeError!
javaObject.doubleArg(1.1); //match, OK
javaObject.intArg(1.1);    //lossy conversion, TypeError!
```


### Method Selection
Java allows method overloading by parameter types. When calling from JavaScript to Java, the method with the narrowest available type that the actual parameters can be losslessly converted to is selected:

```java
//Java
void foo(int arg);
void foo(short arg);
void foo(double arg);
void foo(long arg);
```

```js
//JavaScript
javaObject.foo(1);              // will call foo(short);
javaObject.foo(Math.pow(2,16)); // will call foo(int);
javaObject.foo(1.1);            // will call foo(double);
javaObject.foo(Math.pow(2,32)); // will call foo(long);
```

To override this behavior, you can use the `javaObject['methodName(paramTypes)']` syntax to explicitly select a method overload. Parameter types need to be comma-separated without spaces, and object types need to be fully qualified (e.g., `'get(java.lang.String,java.lang.String[])'`).

```js
javaObject['foo(int)'](1);
javaObject['foo(long)'](1);
javaObject['foo(double)'](1);
```

Note that parameter values must still fit the parameter type. You can use custom target type mappings to override this behavior.

Explicit method selection is also useful when method overloading is ambiguous and cannot be automatically resolved, or when you want to override the default selection:

```java
//Java
void sort(`List<Object>` array, Comparator<Object> callback);
void sort(`List<Integer>` array, IntBinaryOperator callback);
void consumeArray(`List<Object>` array);
void consumeArray(Object[] array);
```

```js
//JavaScript
var array = [3, 13, 3, 7];
var compare = (x, y) => (x < y) ? -1 : ((x == y) ? 0 : 1);

// throws TypeError: Multiple applicable overloads found
javaObject.sort(array, compare);
// explicitly select sort(List, Comparator)
javaObject['sort(java.util.List,java.util.Comparator)'](array, compare);

// will call consumeArray(List)
javaObject.consumeArray(array);
// explicitly select consumeArray(Object[])
javaObject['consumeArray(java.lang.Object[])'](array);
```

> Note that it is currently not possible to explicitly select constructor overloads.


### Array Access
The script engine supports creating Java arrays from JavaScript code. Two patterns are supported:

```js
//Pattern 1
var JArray = Java.type('java.lang.reflect.Array');
var JString = Java.type('java.lang.String');
var sarr = JArray.newInstance(JString, 5);

//Pattern 2
var IntArray = Java.type("int[]");
var iarr = new IntArray(5);
```
The created arrays are Java types but can be used in JavaScript code:

```js
iarr[0] = iarr[iarr.length] * 2;
```

### Map Access
In the script engine, you can create and access Java Maps, such as java.util.HashMap:

```js
var HashMap = Java.type('java.util.HashMap');
var map = new HashMap();
map.put(1, "a");
map.get(1);
```

The script engine supports iterating over such maps:

```js
for (var key in map) {
    print(key);
    print(map.get(key));
}
```

### List Access
In the script engine, you can create and access Java Lists, such as java.util.ArrayList:

```js
var ArrayList = Java.type('java.util.ArrayList');
var list = new ArrayList();
list.add(42);
list.add("23");
list.add({});

for (var idx in list) {
    print(idx);
    print(list.get(idx));
}
```

### String Access
The script engine can create Java strings with Java interoperability. The length of a string can be queried via the `length` property (note that `length` is a value property and cannot be called as a function):

```js
var javaString = new (Java.type('java.lang.String'))("Java");
javaString.length === 4;
```

Note that the script engine internally uses Java strings to represent JavaScript strings, so the above code and the JavaScript string literal "Java" are actually indistinguishable.

### Iterating Properties
Properties (fields and methods) of Java classes and Java objects can be iterated using the JavaScript for..in loop:

```js
var m = Java.type('java.lang.Math')
for (var i in m) { 
    print(i);
}
// > E
// > PI
// > abs
// > sin
// > ...
```
### Complete Example of Using Java Objects in Scripts

```js

//Call Java graphics to draw a rectangle image and return the image as base64 encoding
export function createImage() {
	let width=100;
	let height=100;
	var BufferedImage = Java.type("java.awt.image.BufferedImage");
	var ByteArrayOutputStream=Java.type("java.io.ByteArrayOutputStream");
	var ImageIO=Java.type("javax.imageio.ImageIO");
	var Base64=Java.type("java.util.Base64");
	var Color=Java.type("java.awt.Color");
	//
	var image = new BufferedImage(100, 100, BufferedImage.TYPE_INT_BGR);
	var graphics = image.getGraphics();
	graphics.setColor(new Color(255, 0, 0));
	graphics.fillRect(1, 1, width - 1, height - 1);
	var os=new ByteArrayOutputStream();
	ImageIO.write(image, "jpg", os);
	let content=os.toByteArray();
	let base64=Base64.getEncoder().encodeToString(content);
	return base64;
}
```
## Notes

- 1. File dependencies must include the `.js` file extension
- 2. It is recommended to use relative paths for imports. This way, if `npm` support is added later, no modifications to existing code are needed
  
::::tabs
:::tab Example Directory Structure
  ![Example Directory Structure](images/script-import.png)
:::
:::tab Referencing Script
```javascript
import {success} from "../../../libs/index.js"

export function run(){
    return success();
}
```
:::
:::tab Referenced Script
```javascript
export function success() {
    return "SUCCESS"
}
```
:::
::::

## Additional Notes
- When developing scripts with **VsCode** or **WebStorm**, download [https://next.informat.cn/types/informat.d.ts](https://next.informat.cn/types/informat.d.ts) to get the function description file and resolve code error issues.

- When syncing with git, hidden files starting with `.` will not be synced

- If importing the **informat.d.ts** file into the editor still shows **informat** call errors, create an empty [**jsconfig.json**](https://code.visualstudio.com/docs/languages/jsconfig) file in the project root directory and restart the editor. Set the file content to an empty object as follows:

    ```json
    {}
    ```


