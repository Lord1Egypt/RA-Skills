---
name: java-standards-alibaba
description: Use when writing or modifying Java code — enforces Alibaba Java Development Guidelines (嵩山版) for naming, formatting, OOP, collections, concurrency, control statements, exceptions, logging, MySQL, security, and project structure. Activates for any Java code generation, code review, or code modification task.
---

# Alibaba Java Development Guidelines Skill (嵩山版)

> 在任何 Java 代码的编写、修改、审查场景中，**必须**严格遵守本规范。
> 规约等级：【强制】>【推荐】>【参考】

## 适用范围

本 skill 在以下场景中自动激活并强制执行：

- 编写新的 Java 类 / 接口 / 枚举
- 修改已有的 Java 代码
- 代码审查 / Code Review
- 重构代码
- 生成 SQL / MyBatis XML 映射
- 设计数据库表结构
- 编写单元测试
- 定义 API 接口（前后端交互）

---

## 核心工作流程

### Step 1: 规则匹配

根据当前代码任务，定位适用的规约分类：

| 场景 | 定位规约 |
|------|----------|
| 定义类名/方法名/变量名 | [references/naming.md](references/naming.md) — 命名风格 |
| 定义常量 | [references/constants.md](references/constants.md) — 常量定义 |
| 编写/格式化代码 | [references/code-format.md](references/code-format.md) — 代码格式 |
| 编写类/接口/对象 | [references/oop.md](references/oop.md) — OOP 规约 |
| 处理日期时间 | [references/date-time.md](references/date-time.md) — 日期时间 |
| 使用集合（List/Map/Set） | [references/collections.md](references/collections.md) — 集合处理 |
| 编写并发/多线程代码 | [references/concurrency.md](references/concurrency.md) — 并发处理 |
| 编写条件/循环逻辑 | [references/control-flow.md](references/control-flow.md) — 控制语句 |
| 编写注释 | [references/comments.md](references/comments.md) — 注释规约 |
| 设计 REST API / 前后端交互 | [references/api-contract.md](references/api-contract.md) — 前后端规约 |
| 正则 / BeanUtils / Velocity 等 | [references/others.md](references/others.md) — 其他 |
| 异常处理 / 错误码 | [references/exceptions.md](references/exceptions.md) — 异常日志 |
| 日志打印 | [references/logging.md](references/logging.md) — 日志规约 |
| 编写单元测试 | [references/unit-test.md](references/unit-test.md) — 单元测试 |
| 安全检查 / 输入校验 | [references/security.md](references/security.md) — 安全规约 |
| 建表 / 索引 | [references/mysql-ddl.md](references/mysql-ddl.md) — MySQL 建表规约 |
| 索引设计 | [references/mysql-index.md](references/mysql-index.md) — MySQL 索引规约 |
| 编写 SQL | [references/mysql-sql.md](references/mysql-sql.md) — MySQL SQL 语句 |
| MyBatis / ORM 映射 | [references/orm.md](references/orm.md) — ORM 映射 |
| 项目分层 / 依赖 | [references/project-structure.md](references/project-structure.md) — 工程结构 |
| 系统设计 | [references/design.md](references/design.md) — 设计规约 |

### Step 2: 读取对应规约文件

在生成/修改代码之前，**必须**读取对应 reference 文件，逐条对照【强制】规则。

### Step 3: 生成/修改代码

按照规约要求编写代码，注意：

- 【强制】规则 **必须遵守**，无例外
- 【推荐】规则 **应尽量遵守**
- 【参考】规则 **可酌情采纳**

### Step 4: 自查清单

代码生成后，逐项对照以下通用自查（适用于所有 Java 代码任务）：

#### 命名
- [ ] 类名 `UpperCamelCase`，方法/变量 `lowerCamelCase`
- [ ] 常量全大写 + 下划线分隔
- [ ] 包名全小写，单数形式
- [ ] 无拼音、无下划线开头/结尾、无歧视性词语
- [ ] POJO 布尔变量不加 `is` 前缀
- [ ] 枚举类带 `Enum` 后缀，成员全大写

#### 代码格式
- [ ] 4 空格缩进，无 Tab
- [ ] 单行 ≤ 120 字符
- [ ] 关键词与括号间有空格，运算符左右有空格
- [ ] UTF-8 编码，Unix 换行符

#### OOP
- [ ] 覆写方法加了 `@Override`
- [ ] `equals` 用常量/确定值调用，整型包装类用 `equals` 比较
- [ ] 浮点数用 `BigDecimal` 比较，`BigDecimal` 用 `compareTo`
- [ ] POJO 属性用包装类型，不设默认值
- [ ] POJO 有 `toString`
- [ ] 构造方法无业务逻辑

#### 集合
- [ ] 覆写 `equals` 时覆写了 `hashCode`
- [ ] `isEmpty()` 判空而非 `size()==0`
- [ ] `Collectors.toMap()` 使用了 `mergeFunction`
- [ ] `foreach` 中无 `remove/add` 操作
- [ ] 集合初始化指定大小

#### 并发
- [ ] 线程通过线程池创建，不用 `Executors`
- [ ] `SimpleDateFormat` 非 static 或用 `ThreadLocal`
- [ ] `ThreadLocal` 在 `finally` 中 `remove()`
- [ ] 锁在 `try` 外获取，`finally` 中释放

#### 控制语句
- [ ] `switch` 有 `default`，每个 `case` 有 `break/return`
- [ ] `if/else/for/while` 使用大括号
- [ ] 三目运算符注意自动拆箱 NPE

#### 异常日志
- [ ] 不用 catch 预检可规避的 RuntimeException
- [ ] 异常不捕获后抛弃，要处理或上抛
- [ ] finally 中不使用 return
- [ ] RPC/二方包用 `Throwable` 拦截
- [ ] 日志用 SLF4J，占位符拼接，有级别开关
- [ ] 生产环境无 `System.out` / `e.printStackTrace()`

#### MySQL
- [ ] 不用 `SELECT *`
- [ ] 主键 `bigint unsigned` 自增，必备字段 `id, create_time, update_time`
- [ ] 小数用 `decimal`，不用 `float/double`
- [ ] 无外键、无存储过程
- [ ] MyBatis 用 `#{}` 不用 `${}`

#### 安全
- [ ] SQL 参数绑定，无字符串拼接
- [ ] 用户输入参数校验
- [ ] 敏感数据脱敏
- [ ] CSRF 防护

---

## 快速规则速查

### 命名速查

```
类名:       UpperCamelCase   (例外: DO/DTO/VO/BO/AO/PO/UID)
方法/变量:  lowerCamelCase
常量:       ALL_UPPER_CASE
包名:       alllowercase.singular
数组:       int[] array      (不是 String args[])
枚举:       XxxEnum.SOME_VALUE
抽象类:     AbstractXxx / BaseXxx
异常类:     XxxException
测试类:     XxxTest
Service:    XxxService (接口) / XxxServiceImpl (实现)
```

### 代码格式速查

```
缩进:       4 空格，禁止 Tab
行宽:       ≤ 120 字符
空格:       if/for/while + 空格 + (
           运算符左右各一空格
           注释 // 后一空格
括号:       左大括号前空格，不换行
编码:       UTF-8，Unix 换行
```

### 常见陷阱速查

| 陷阱 | 正确做法 |
|------|----------|
| `Integer a == Integer b` | `a.equals(b)` |
| `float a == float b` | `Math.abs(a-b) < epsilon` 或 `BigDecimal` |
| `BigDecimal(double)` | `new BigDecimal("0.1")` 或 `BigDecimal.valueOf(0.1)` |
| `BigDecimal.equals()` | `BigDecimal.compareTo()` |
| `new Date().getTime()` | `System.currentTimeMillis()` |
| `SimpleDateFormat` static | `ThreadLocal<DateFormat>` 或 `DateTimeFormatter` |
| `Executors.newFixedThreadPool()` | `new ThreadPoolExecutor(...)` |
| `foreach` 中 `list.remove()` | `iterator.remove()` |
| `catch(Exception e) { }` | 处理异常或上抛 |
| `finally { return x; }` | 不在 finally 中 return |
| `SELECT *` | 明确列出字段 |
| MyBatis `${param}` | `#{param}` |
| 魔法值直接写 | 定义为常量 |
| POJO `boolean isDeleted` | `Boolean deleted` (POJO 不用 is 前缀) |
| `long a = 2l` | `long a = 2L` (大写 L) |

---

## 参考文件

完整规约来源: `D:\ai\Java开发手册（嵩山版）.md`

| 文件 | 内容 |
|------|------|
| [references/naming.md](references/naming.md) | 命名风格（19 条） |
| [references/constants.md](references/constants.md) | 常量定义（5 条） |
| [references/code-format.md](references/code-format.md) | 代码格式（13 条） |
| [references/oop.md](references/oop.md) | OOP 规约（26 条） |
| [references/date-time.md](references/date-time.md) | 日期时间（7 条） |
| [references/collections.md](references/collections.md) | 集合处理（21 条） |
| [references/concurrency.md](references/concurrency.md) | 并发处理（19 条） |
| [references/control-flow.md](references/control-flow.md) | 控制语句（14 条） |
| [references/comments.md](references/comments.md) | 注释规约（12 条） |
| [references/api-contract.md](references/api-contract.md) | 前后端规约（14 条） |
| [references/others.md](references/others.md) | 其他（8 条） |
| [references/exceptions.md](references/exceptions.md) | 异常处理（13 条）+ 错误码（13 条） |
| [references/logging.md](references/logging.md) | 日志规约（13 条） |
| [references/unit-test.md](references/unit-test.md) | 单元测试（16 条） |
| [references/security.md](references/security.md) | 安全规约（9 条） |
| [references/mysql-ddl.md](references/mysql-ddl.md) | MySQL 建表规约（15 条） |
| [references/mysql-index.md](references/mysql-index.md) | MySQL 索引规约（11 条） |
| [references/mysql-sql.md](references/mysql-sql.md) | MySQL SQL 语句（13 条） |
| [references/orm.md](references/orm.md) | ORM 映射（10 条） |
| [references/project-structure.md](references/project-structure.md) | 工程结构（20 条） |
| [references/design.md](references/design.md) | 设计规约（19 条） |

---

## 版本

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1.0.0 | 2026-04-29 | endcy | 初始版本，基于嵩山版（1.7.0）完整规约 |
