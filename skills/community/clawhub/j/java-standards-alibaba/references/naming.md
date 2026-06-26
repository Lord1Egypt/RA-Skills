# 命名风格

> 来源: Java开发手册（嵩山版）— 一(一) 命名风格

## 【强制】规则

### 1. 禁止下划线/美元符号开头或结尾

代码中的命名均不能以下划线或美元符号开始，也不能以下划线或美元符号结束。

> **反例**: `_name` / `__name` / `$name` / `name_` / `name$` / `name__`

### 2. 禁止拼音与英文混合，禁止中文

所有编程相关的命名严禁使用拼音与英文混合的方式，更不允许直接使用中文的方式。

> **说明**: 纯拼音命名方式更要避免采用。  
> **正例**: `ali` / `alibaba` / `taobao` / `cainiao` / `aliyun` / `youku` / `hangzhou` 等国际通用名称  
> **反例**: `DaZhePromotion` / `getPingfenByName()` / `String fw` / `int 某变量 = 3`

### 3. 禁止歧视性词语

代码和注释中都要避免使用任何语言的种族歧视性词语。

> **正例**: `blockList` / `allowList` / `secondary`  
> **反例**: `blackList` / `whiteList` / `slave`

### 4. 类名 UpperCamelCase

类名使用 `UpperCamelCase` 风格，但以下情形例外：`DO` / `BO` / `DTO` / `VO` / `AO` / `PO` / `UID` 等。

> **正例**: `ForceCode` / `UserDO` / `HtmlDTO` / `XmlService` / `TcpUdpDeal`  
> **反例**: `forcecode` / `UserDo` / `HTMLDto` / `XMLService` / `TCPUDPDeal`

### 5. 方法名/参数名/变量名 lowerCamelCase

方法名、参数名、成员变量、局部变量都统一使用 `lowerCamelCase` 风格。

> **正例**: `localValue` / `getHttpMessage()` / `inputUserId`

### 6. 常量全大写 + 下划线

常量命名全部大写，单词间用下划线隔开，力求语义表达完整清楚，不要嫌名字长。

> **正例**: `MAX_STOCK_COUNT` / `CACHE_EXPIRED_TIME`  
> **反例**: `MAX_COUNT` / `EXPIRED_TIME`

### 7. 特殊类命名

- 抽象类: `Abstract` 或 `Base` 开头
- 异常类: `Exception` 结尾
- 测试类: 以被测试类名开头，以 `Test` 结尾

### 8. 数组类型声明

类型与中括号紧挨相连来表示数组。

> **正例**: `int[] arrayDemo`  
> **反例**: `String args[]`

### 9. POJO 布尔变量不加 is 前缀

POJO 类中的任何布尔类型的变量，都不要加 `is` 前缀，否则部分框架解析会引起序列化错误。

> **说明**: 需要在 `<resultMap>` 设置从 `is_xxx` 到 `xxx` 的映射关系。  
> **反例**: `Boolean isDeleted` → 框架误以为属性名是 `deleted`

### 10. 包名全小写 + 单数

包名统一使用小写，点分隔符之间有且仅有一个自然语义的英语单词。包名统一使用单数形式。

> **正例**: `com.alibaba.ei.kunlun.aap.util`

### 11. 避免子父类/不同代码块中同名

杜绝在子父类的成员变量之间、或者不同代码块的局部变量之间采用完全相同的命名。

### 12. 杜绝不规范缩写

> **反例**: `AbstractClass` → `AbsClass`；`condition` → `condi`；`Function` → `Fu`

## 【推荐】规则

### 13. 命名使用完整单词组合

> **正例**: `AtomicReferenceFieldUpdater`  
> **反例**: `int a;`

### 14. 类型名词放词尾

> **正例**: `startTime` / `workQueue` / `nameList` / `TERMINATED_THREAD_COUNT`  
> **反例**: `startedAt` / `QueueOfWork` / `listName`

### 15. 命名体现设计模式

> **正例**: `OrderFactory` / `LoginProxy` / `ResourceObserver`

### 16. 接口方法和属性不加修饰符

接口类中的方法和属性不要加任何修饰符号（`public` 也不要加），保持代码的简洁性，并加上有效的 Javadoc 注释。

> **正例**: `void commit();` / `String COMPANY = "alibaba";`  
> **反例**: `public abstract void f();`

### 17. Service/DAO 命名

1. **接口与实现**: Service 和 DAO 类，接口不加后缀，实现类用 `Impl` 后缀。
   > **正例**: `CacheServiceImpl` 实现 `CacheService`
2. **能力接口**: 取对应形容词（通常是 `–able`）。
   > **正例**: `Translatable` 接口

### 18. 枚举命名

枚举类名带 `Enum` 后缀，枚举成员名称全大写，单词间用下划线隔开。

> **正例**: `ProcessStatusEnum` 的成员: `SUCCESS` / `UNKNOWN_REASON`

### 19. 各层命名规约

**Service/DAO 层方法命名**:

| 操作 | 前缀 |
|------|------|
| 获取单个对象 | `get` |
| 获取多个对象 | `list` (复数结尾) |
| 获取统计值 | `count` |
| 插入 | `save/insert` |
| 删除 | `remove/delete` |
| 修改 | `update` |

**领域模型命名**:

| 类型 | 命名 | 说明 |
|------|------|------|
| 数据对象 | `xxxDO` | xxx 为数据表名 |
| 数据传输对象 | `xxxDTO` | xxx 为业务领域名称 |
| 展示对象 | `xxxVO` | xxx 一般为网页名称 |
| 统称 | `POJO` | 禁止命名成 `xxxPOJO` |
