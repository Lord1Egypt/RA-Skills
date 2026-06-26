# 其他

> 来源: Java开发手册（嵩山版）— 一(十一) 其他

## 【强制】规则

### 1. 正则预编译

利用预编译功能加快匹配速度。不要在方法体内定义 `Pattern pattern = Pattern.compile("规则");`

### 2. 避免 Apache BeanUtils

性能较差，可使用 Spring BeanUtils 或 Cglib BeanCopier（均是浅拷贝）。

### 3. Velocity 模板取值

直接写属性名即可，模板引擎会自动调用 `getXxx()`。Boolean 包装类优先调用 `getXxx()`。

### 4. Velocity 变量加感叹号

后台输送给页面的变量必须加 `$!{var}` —— 中间的感叹号。

> **说明**: 如果 var 为 null，`${var}` 会直接显示在页面上。

### 5. Math.random() 注意

返回 `double`，范围 `0 <= x < 1`。想获取整数随机数，使用 `Random.nextInt/nextLong`。

## 【推荐】规则

### 6. 视图模板无复杂逻辑

视图的职责是展示，不要抢模型和控制器的活。

### 7. 数据结构指定大小

避免数据结构无限增长吃光内存。

### 8. 清理不再使用的代码

对于垃圾代码或过时配置，坚决清理干净。
