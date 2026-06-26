# magic-script 语法参考

## 目录
- [变量与类型](#变量与类型)
- [运算符](#运算符)
- [控制流](#控制流)
- [函数定义](#函数定义)
- [字符串方法](#字符串方法)
- [列表方法](#列表方法)
- [Map 方法](#map-方法)
- [日期处理](#日期处理)
- [Java 类导入](#java-类导入)

## 变量与类型

```javascript
// 基本类型
var num = 123;              // 数字
var str = "hello";          // 字符串
var bool = true;            // 布尔
var list = [1, 2, 3];       // 列表
var map = {a: 1, b: 2};     // Map
var empty = null;           // null

// 类型判断
val instanceof String       // true/false
typeof(val)                 // "string"/"number"/"boolean"...
```

## 运算符

```javascript
// 算术
10 + 5    // 15
10 - 5    // 5
10 * 5    // 50
10 / 5    // 2
10 % 3    // 1

// 比较
1 == "1"    // true（值相等）
1 === 1     // true（严格相等）
1 != 2      // true
1 !== "1"   // true

// 逻辑
true && false   // false
true || false   // true
!true           // false

// 空值合并
null ?? "default"     // "default"
"value" ?? "default"  // "value"
```

## 控制流

```javascript
// if-else
if (score >= 90) {
    return "A";
} else if (score >= 60) {
    return "B";
} else {
    return "C";
}

// for 循环
for (var i = 0; i < 10; i++) {
    log.info(i);
}

// for-in 循环
for (var item in list) {
    log.info(item);
}

// while 循环
var i = 0;
while (i < 10) {
    i++;
}

// 异常处理
try {
    var result = db.select("select * from user");
} catch (e) {
    log.error("错误: " + e.message);
    return {code: 500, msg: "系统错误"};
}
```

## 函数定义

```javascript
// 普通函数
function add(a, b) {
    return a + b;
}

// 箭头函数
var add = (a, b) => a + b;

// 默认参数
function greet(name = "World") {
    return "Hello, " + name;
}

// Lambda
var list = [1, 2, 3, 4, 5];
list.map(x => x * 2);           // [2, 4, 6, 8, 10]
list.filter(x => x % 2 == 0);   // [2, 4]
list.reduce((acc, x) => acc + x, 0);  // 15
```

## 字符串方法

```javascript
var str = "Hello World";

str.length()                // 11
str.toLowerCase()           // "hello world"
str.toUpperCase()           // "HELLO WORLD"
str.trim()                  // 去首尾空格
str.substring(0, 5)         // "Hello"
str.split(" ")              // ["Hello", "World"]
str.replace("World", "API") // "Hello API"
str.indexOf("World")        // 6
str.startsWith("Hello")     // true
str.endsWith("World")       // true
str.contains("lo")          // true
```

## 列表方法

```javascript
var list = [1, 2, 3, 4, 5];

list.length()               // 5
list.push(6)                // 添加元素到末尾
list.pop()                  // 弹出最后一个
list.shift()                // 弹出第一个
list.reverse()              // 反转
list.join(",")              // "1,2,3,4,5"
list.contains(3)            // true
list.indexOf(3)             // 2
list.remove(3)              // 删除元素 3
```

## Map 方法

```javascript
var map = {name: "张三", age: 25};

map.size()                  // 2
map.get("name")             // "张三"
map.put("city", "北京")      // 添加/更新
map.remove("age")           // 删除
map.containsKey("name")     // true
map.keySet()                // ["name", "city"]
map.values()                // ["张三", "北京"]
```

## 日期处理

```javascript
var now = new Date();

now.getFullYear()           // 年
now.getMonth()              // 月 (0-11)
now.getDate()               // 日
now.getHours()              // 时
now.getMinutes()            // 分
now.getSeconds()            // 秒
now.getTime()               // 时间戳

// 格式化
now.format("yyyy-MM-dd")           // "2024-01-01"
now.format("yyyy-MM-dd HH:mm:ss")  // "2024-01-01 12:30:00"

// 解析
Date.parse("2024-01-01", "yyyy-MM-dd")

// 时间戳
Date.now()                  // 当前时间戳
new Date(1704067200000)     // 从时间戳创建
```

## Java 类导入

```javascript
// 导入 Java 类
var ArrayList = import('java.util.ArrayList');
var list = new ArrayList();
list.add("item");

// 导入工具类
var Math = import('java.lang.Math');
Math.max(1, 2);             // 2
Math.random();              // 随机数

// 导入 Spring Bean
var userService = bean('userService');
var user = userService.findById(1);

// UUID
var UUID = import('java.util.UUID');
UUID.randomUUID().toString()

// MD5 加密
var MessageDigest = import('java.security.MessageDigest');
var md = MessageDigest.getInstance("MD5");
md.digest("password".getBytes());
```
