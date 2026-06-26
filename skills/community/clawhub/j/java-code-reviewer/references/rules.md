# Java 代码审查规则（精简版）

## 一、Google Java Style Guide 精简（10条）

### 1. 命名规范
- **类名**：UpperCamelCase，如 `UserService`
- **方法名/变量名**：lowerCamelCase，如 `getUserById`
- **常量**：CONSTANT_CASE，如 `MAX_RETRY_COUNT`
- **包名**：全小写，如 `com.example.service`

### 2. 源文件结构
- 顺序：License → package → import → 类声明
- import 不用通配符，按字母排序

### 3. 注释
- 公共 API 必须有 Javadoc
- 注释解释"为什么"，不解释"是什么"
- 删除注释掉的代码

### 5. 编程实践
- @Override 必须加（实现接口或继承父类时）
- 静态成员用类名调用，不用对象
- 先检查参数有效性

### 6. 禁止用法
- 不要使用 `==` 比较对象，用 `equals()`
- 不要使用 `goto`
- 避免使用可变参数替代重载

### 7. 注解
- 注解紧跟在声明前
- 单个注解可不换行

### 8. 命名约定
- 避免缩写（除非业界通用如 `id`, `url`）
- 布尔变量避免否定命名，如 `isNotEmpty` → `hasElements`

### 9. 字符串与资源
- 使用 `""` 而非 `new String("")`
- 字符串拼接用 StringBuilder（非循环内）
- 同一包内不 import

---

## 二、阿里巴巴 Java 开发手册 精简（10条）

### 1. 命名
- 抽象类以 Abstract 或 Base 开头
- 接口以 I 开头或 +able/-er 后缀
- 枚举类以 Enum 结尾，成员全大写

### 2. 常量
- 不允许魔法值（直接写数字/字符串）
- long 类型 L 大写（避免 1 和 l 混淆）

### 3. OOP
- 覆写方法必须加 @Override
- 相同参数类型、相同业务含义使用可变参数
- 外部正在调用或调用的接口，不允许修改方法签名

### 4. 集合
- 使用 `HashMap` 的 `computeIfAbsent` 简化逻辑
- 使用 `Collection.isEmpty()` 判断空集合
- 集合返回值用 `ArrayList` 而非 `List`

### 5. 并发
- 创建线程或线程池必须指定有意义的名称
- 多线程调用 ThreadLocal 必须 initialValue
- 优先使用 CompletableFuture 异步处理

### 6. 异常
- 异常捕获不要只 catch Exception
- 捕获异常后必须处理或抛出
- finally 中必须关闭资源

### 7. 日志
- 日志级别：ERROR（影响功能）、WARN（可恢复问题）、INFO（关键流程）
- 使用 SLF4J 参数化日志，禁止字符串拼接：
  ```java
  // ✅ 正确
  log.info("userId: {}, orderId: {}", userId, orderId);
  // ❌ 错误
  log.info("userId: " + userId + ", orderId: " + orderId);
  ```

### 8. 安全
- 敏感信息必须脱敏
- 避免 SQL 注入，使用参数化查询
- 敏感请求必须校验

### 9. MyBatis
- `#{}` 防止 SQL 注入
- `<where>` 标签避免多余 AND/OR
- 关联查询用 resultMap

### 10. 单元测试
- 测试类以 Test 结尾
- 测试方法以 test 开头
- 保持测试用例独立

---

## 三、Clean Code 原则 精简（10条）

### 1. 命名
- 变量名有意义：`int d` → `int daysSinceCreation`
- 函数名表达做什么：`getUser()` → `getUserById()`
- 类名是名词，方法名是动词

### 2. 函数
- 短小：一个函数只做一件事
- 参数少：最好 0-2 个，3 个尽量避免
- 不重复代码（DRY）

### 3. 注释
- 好代码 > 坏代码 + 好注释
- 注释解释意图，不是翻译代码
- 必要的注释：法律、解释复杂业务、警示

### 4. 格式
- 垂直格式：一屏显示一个方法
- 水平格式：相关代码放一起
- 变量靠近使用处声明

### 5. 错误处理
- 用异常而非返回码
- 异常信息要描述来源和原因
- 别返回 null，别传 null

### 6. 边界
- 避免硬编码外部接口
- 封装外部调用为接口

### 7. 单元测试
- 测试覆盖所有代码路径
- 测试是代码的第一个用户
- F.I.R.S.T 原则：Fast, Independent, Repeatable, Self-Validating, Timely

### 8. 类
- 单一职责：一个类一个改变理由
- 高内聚：类成员相关性高
- 依赖倒置：依赖抽象而非具体

### 9. 并发
- 分离并发相关代码与非并发代码
- 用数据封装减少同步
- 了解所有可能的执行路径

### 10. 魔法数字
- 禁止在代码中直接使用数字字面量，应定义为命名常量
- ```java
  // ❌ 错误
  if (user.getAge() > 18) { ... }
  // ✅ 正确
  private static final int ADULT_AGE = 18;
  if (user.getAge() > ADULT_AGE) { ... }
  ```

### 11. 代码味道
- 重复代码
- 过长的函数
- 过多的参数
- 全局数据
- 特性依恋（一个类过度关注其他类）
