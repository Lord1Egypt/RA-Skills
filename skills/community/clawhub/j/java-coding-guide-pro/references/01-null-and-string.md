# 01 · Null 安全与字符串

> **Null 安全**：JDK `Optional`/`Objects`（原生完善→用原生）+ `ObjectUtil.equal`（防 NPE）。
> **字符串**：Hutool `StrUtil`（`cn.hutool.core.util.StrUtil`，继承 `CharSequenceUtil`）。

## 规范速查

| 场景 | ✗ 禁止 | ✓ 推荐 |
|---|---|---|
| 字符串判空白 | `str == null \|\| str.trim().isEmpty()` | `StrUtil.isBlank(str)` |
| 字符串判非空白 | `str != null && !str.trim().isEmpty()` | `StrUtil.isNotBlank(str)` |
| 任一为空白 | `a == null \|\| b == null` 手写 | `StrUtil.hasBlank(a, b)` |
| 空白时给默认值 | `str != null ? str : "def"`（纯空格漏判） | `StrUtil.blankToDefault(str, "def")` |
| 仅 null/"" 时给默认值 | 同上手写 | `StrUtil.emptyToDefault(str, "def")`（不判空格） |
| 相等（防 NPE） | `a.equals(b)` | `ObjectUtil.equal(a, b)` / `"常量".equals(a)` |
| 忽略大小写相等 | `a.equalsIgnoreCase(b)` | `StrUtil.equalsIgnoreCase(a, b)` |
| 格式化 | `String.format("%s/%s", a, b)` | `StrUtil.format("{}/{}", a, b)` |
| 去两端空白 | `s.trim()` | `StrUtil.trim(s)` |
| 去两端空白，全空则 null | 手写三元 | `StrUtil.trimToNull(s)` |
| 去所有空白字符 | `s.replaceAll("\\s+", "")` | `StrUtil.cleanBlank(s)` |
| 截取（防越界） | `s.substring(s.indexOf("-")+1)` | `StrUtil.subAfter(s, "-", false)` |
| 分隔 | `s.split(".")`（正则坑） | `StrUtil.split(s, '.')` → `List<String>` |
| 拼接集合 | 手写 for+StringBuilder | `StrUtil.join(",", list)` |
| 驼峰→下划线 | 手写正则 | `StrUtil.toUnderlineCase(s)` |
| 下划线→驼峰 | 手写正则 | `StrUtil.toCamelCase(s)` |
| 首字母大写 | 手写 | `StrUtil.upperFirst(s)` |
| HTML 转义 | 手写 | **`HtmlUtil.escapeHtml(s)`**（`cn.hutool.core.util.HtmlUtil`，非 StrUtil） |

## 反例详解（antipattern）

### 1. `isBlank` vs `isEmpty` 空格陷阱
```java
// ✗ " "（纯空格）判为"非空"，后续逻辑可能出错
if (str != null && !str.isEmpty()) { ... }

// ✓ 空白（空格/制表符/换行）统一视为空，符合业务直觉
if (StrUtil.isNotBlank(str)) { ... }
```

### 2. `equals` 可能 NPE
```java
// ✗ str 为 null 抛 NullPointerException
if (str.equals("admin")) { ... }

// ✓ null 安全
if ("admin".equals(str)) { ... }       // 常量在前
if (StrUtil.equals(str, "admin")) { ... } // 工具方法
```

### 3. `substring` 越界
```java
// ✗ indexOf 返回 -1 时 substring 抛 StringIndexOutOfBoundsException
String v = s.substring(s.indexOf("-") + 1);

// ✓ StrUtil 越界安全，取不到返回空串
String v = StrUtil.subAfter(s, "-", false); // 第三参 isLastSeparator
```

### 4. `split` 正则转义坑
```java
// ✗ "." 是正则元字符，split(".") 结果为空数组
String[] ps = s.split(".");

// ✓ StrUtil.split 按字面量分割，返回 List
List<String> ps = StrUtil.split(s, '.');
```

### 5. `emptyToDefault` vs `blankToDefault`（注意语义差异）
```java
// 两者都存在，语义不同：
StrUtil.emptyToDefault("   ", "x");  // 返回 "   "（仅判 null/""，不判空格）
StrUtil.blankToDefault("   ", "x");  // 返回 "x"  （判 null/""/纯空白）

// 推荐 blankToDefault，与 isBlank 规范一致
```

## Optional 使用规范（防滥用）

```java
// ✗ 不判空直接 get → NoSuchElementException
User u = findUser(id).get();

// ✓ orElse 提供默认值 / orElseThrow 明确异常
User u = findUser(id).orElse(defaultUser);
User u = findUser(id).orElseThrow(() -> new BizException("不存在"));

// ✗ Optional 作字段/参数类型（设计反模式）
// ✓ Optional 仅作返回值，表达"可能无值"

// ✓ 链式处理
String name = findUser(id)
    .map(User::getName)
    .filter(StrUtil::isNotBlank)
    .orElse("匿名");
```

## 推荐示例

```java
// 判空 + 默认值
String name = StrUtil.blankToDefault(userInput, "anonymous");

// 格式化（{} 占位，slf4j 风格）
String path = StrUtil.format("/user/{}/order/{}", uid, orderId);

// 取后缀（越界安全）
String ext = StrUtil.subAfter(fileName, ".", true); // isLastSeparator=true 取最后一个点

// 集合拼接
String ids = StrUtil.join(",", userIds);

// 命名转换
String column = StrUtil.toUnderlineCase("userName"); // user_name
String camel  = StrUtil.toCamelCase("user_name");     // userName
```

## Sonar java:S3252 与 StrUtil（默认保留 StrUtil）

Hutool 5.5.3+ 把字符串方法上移至 `CharSequenceUtil`，`StrUtil` 作为官方门面继承保留，故 `StrUtil.isBlank` 会命中 S3252。该规则本意是防「偶然继承」，而 `StrUtil` 是有意设计的门面（官方统一入口、更短可读）——**默认继续写 `StrUtil`，不主动改写**。

仅当项目门禁启用该规则且阻断交付时二选一（全项目统一、禁混用、禁逐处 NOSONAR）：
1. 质量平台将 Hutool 门面告警标 Accepted / 配置规则例外（推荐，一次配置全局生效）；
2. 全局改用定义类 `CharSequenceUtil`。

> 同类门面（`DateUtil extends CalendarUtil`、`ArrayUtil extends PrimitiveArrayUtil`）同策略。
