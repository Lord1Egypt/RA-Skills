# OOP 规约

> 来源: Java开发手册（嵩山版）— 一(四) OOP 规约

## 【强制】规则

### 1. 静态成员通过类名访问

避免通过对象引用访问静态变量或静态方法，直接用类名来访问。

### 2. 覆写方法加 @Override

所有的覆写方法，必须加 `@Override` 注解。

### 3. 可变参数避免 Object

相同参数类型、相同业务含义，才可以使用可变参数，避免使用 `Object`。可变参数必须放在参数列表最后。

> **正例**: `public List<User> listUsers(String type, Long... ids)`

### 4. 不修改已暴露接口签名

外部正在调用或二方库依赖的接口，不允许修改方法签名。接口过时必须加 `@Deprecated` 注解，并说明新接口。

### 5. 不使用过时类或方法

### 6. equals 用常量调用

`Object` 的 `equals` 方法容易抛空指针，应使用常量或确定有值的对象来调用。

> **正例**: `"test".equals(object)`  
> **说明**: 推荐 `java.util.Objects#equals(Object a, Object b)`

### 7. 整型包装类用 equals 比较

所有整型包装类对象之间值的比较，全部使用 `equals` 方法。

> **说明**: Integer 在 -128~127 之间复用对象，区间外在堆上产生，`==` 判断是陷阱。

### 8. 货币金额用最小单位整型

任何货币金额，均以最小货币单位且整型类型来进行存储。

### 9. 浮点数不用 == 和 equals 比较

基本数据类型不能用 `==`，包装数据类型不能用 `equals`。

> **正例**:
> ```java
> // 方式一: 误差范围
> if (Math.abs(a - b) < 1e-6F) { }
> // 方式二: BigDecimal
> BigDecimal a = new BigDecimal("1.0");
> if (a.compareTo(b) == 0) { }
> ```

### 10. BigDecimal 比较用 compareTo

`equals()` 会比较值和精度（1.0 与 1.00 返回 false），`compareTo()` 忽略精度。

### 11. DO 属性类型匹配数据库字段

> **反例**: 数据库 `bigint unsigned` 对应类属性应为 `Long`，误用 `Integer` 会溢出。

### 12. BigDecimal 不用 double 构造

禁止使用 `BigDecimal(double)`，存在精度损失。优先 `new BigDecimal("0.1")` 或 `BigDecimal.valueOf(0.1)`。

### 13. POJO 用包装类型 / RPC 用包装类型 / 局部变量用基本类型

1. **【强制】** 所有 POJO 类属性必须使用包装数据类型
2. **【强制】** RPC 方法的返回值和参数必须使用包装数据类型
3. **【推荐】** 所有局部变量使用基本数据类型

### 14. POJO 不设属性默认值

> **反例**: `createTime` 默认值为 `new Date()`，更新其他字段时会附带更新此字段。

### 15. 序列化不修改 serialVersionUID

序列化类新增属性时，不要修改 `serialVersionUID` 字段。

### 16. 构造方法无业务逻辑

构造方法里面禁止加入任何业务逻辑，初始化逻辑放在 `init` 方法中。

### 17. POJO 必须写 toString

使用 IDE 生成 toString 时，如果继承了另一个 POJO 类，注意加 `super.toString`。

### 18. POJO 不同时存在 isXxx() 和 getXxx()

禁止在 POJO 类中同时存在对应属性 xxx 的 `isXxx()` 和 `getXxx()` 方法。

## 【推荐】规则

### 19. split 数组末尾检查

使用索引访问 `split` 得到的数组时，需做最后一个分隔符后有无内容的检查。

### 20. 重载方法按序放置

多个构造方法或多个同名方法，应该按顺序放置在一起。

### 21. 类内方法定义顺序

公有方法/保护方法 > 私有方法 > getter/setter 方法。

### 22. getter/setter 无业务逻辑

setter 中 `this.成员名 = 参数名`。getter/setter 中不要增加业务逻辑。

### 23. 循环内字符串拼接用 StringBuilder

> **反例**: `str = str + "hello";` 在循环中每次 new StringBuilder，造成内存浪费。

### 24. final 使用场景

1. 不允许被继承的类（如 String）
2. 不允许修改引用的域对象
3. 不允许被覆写的方法
4. 不允许重新赋值的局部变量
5. 避免上下文重复使用变量

### 25. 慎用 Object.clone

对象 `clone` 默认是浅拷贝，深拷贝需覆写 `clone` 方法。

### 26. 访问控制从严

| 场景 | 修饰符 |
|------|--------|
| 不允许外部 new | `private` 构造方法 |
| 工具类 | 不允许 `public`/`default` 构造方法 |
| 与子类共享的非 static 成员 | `protected` |
| 仅本类使用的非 static 成员 | `private` |
| 仅本类使用的 static 成员 | `private` |
| static 成员考虑 | `final` |
| 仅内部调用的方法 | `private` |
| 仅对继承类公开的方法 | `protected` |
