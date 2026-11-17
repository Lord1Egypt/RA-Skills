# 03 · SpotBugs 与 FindSecBugs 安全扫描

PMD 分析源码 AST，SpotBugs 分析**字节码**（能发现 PMD 看不到的空指针数据流、资源泄漏、序列化陷阱等）。FindSecBugs 是 SpotBugs 的安全插件，覆盖 138 类漏洞。本文给高频 bug pattern 与安全规则的修复速查。**运行前必须先编译**（`mvn compile`），坐标与 pom 见 `01-setup.md`。

## 一、SpotBugs 报告解读

报告 `spotbugsXml.xml` 中每个 `<BugInstance>` 关键属性：
- `type`：bug 模式代码（如 `NP_NULL_ON_SOME_PATH`）。
- `category`：`CORRECTNESS` / `SECURITY` / `BAD_PRACTICE` / `MT_CORRECTNESS` / `PERFORMANCE` 等。
- `rank`：1–20，**1–4 = Scariest，5–9 = Scary，10–14 = Troubling，15–20 = Of Concern**（SpotBugs 官方分档）。门禁分级以 rank 为准（换算见 `04-fix-workflow.md`）。
- `priority`：1/2/3（SpotBugs 内部置信度，1 最高），与 rank 不同，仅作参考。
- 根节点 `<Plugin id='com.h3xstream.findsecbugs' enabled='true'>` 表示 FindSecBugs 已加载。

## 二、SpotBugs 高频 bug pattern → 修复速查

| type | 含义 | ✓ 修复 |
|---|---|---|
| `NP_NULL_ON_SOME_PATH` | 某路径上解引用可能为 null 的值 | 前置判空 / `Optional` / `Objects.requireNonNull` |
| `NP_NULL_PARAM_DEREF` | 可能传 null 的参数被解引用 | 调用侧保证非 null，或方法内判空 |
| `NP_NULL_ON_SOME_PATH_FROM_RETURN_VALUE` | 未判空就用可能返回 null 的方法结果 | 先接收再判空 |
| `RCN_REDUNDANT_NULLCHECK_OF_NONNULL_VALUE` | 冗余判空（前面已解引用） | 删除冗余判空或修正逻辑顺序 |
| `EI_EXPOSE_REP` / `EI_EXPOSE_REP2` | getter 返回内部可变对象 / 构造直接存引用 | 返回/存储防御性拷贝 |
| `DM_DEFAULT_ENCODING` | `getBytes()`/`new String(byte[])` 依赖平台默认编码 | 显式指定 `StandardCharsets.UTF_8` |
| `DM_BOXED_PRIMITIVE_FOR_PARSING` | `new Integer(s)` / `Integer(s).intValue()` 解析 | `Integer.parseInt(s)` |
| `DMI_BIGDECIMAL_CONSTRUCTED_FROM_DOUBLE` | `new BigDecimal(0.1)` | `new BigDecimal("0.1")` / `valueOf`（与 PMD 重叠，任一层报出即修） |
| `ES_COMPARING_PARAMETER_STRING_WITH_EQ` | 字符串用 `==` 比较 | `equals` / `Objects.equals` |
| `OBL_UNSATISFIED_OBLIGATION` | 资源未确保关闭 | try-with-resources |
| `SIC_INNER_SHOULD_BE_STATIC` | 内部类未持有外部引用却非 static | 声明为 `static` 内部类 |
| `SE_NO_SERIALVERSIONID` | Serializable 类缺 serialVersionUID | 加 `serialVersionUID` |
| `RV_RETURN_VALUE_IGNORED_BAD_PRACTICE` | 忽略重要返回值（如 `File.delete()`） | 检查返回值并处理失败分支 |
| `ICAST_IDIV_CAST_TO_DOUBLE` | 整数相除再转 double（精度丢失） | 先转 double 再除 |
| `SF_SWITCH_FALLTHROUGH` | switch 分支缺 break 意外贯穿 | 补 `break` 或注释标注有意贯穿 |

## 三、FindSecBugs 安全规则重点 → 修复速查

安全类告警（`category='SECURITY'`）**Agent 不得自行豁免**，只能修复或如实上报（见 `04-fix-workflow.md`）。所有修复手法已内联，单装本技能即可闭环。

| type | 漏洞 | ✓ 修复 |
|---|---|---|
| `SQL_INJECTION_JDBC` / `SQL_NONCONSTANT_STRING_PASSED_TO_EXECUTE` | SQL 注入（字符串拼接 SQL） | `PreparedStatement` + 参数占位 `?`，禁止拼接；MyBatis 用 `#{}` 不用 `${}` |
| `SQL_INJECTION_SPRING_JDBC` / `_HIBERNATE` | ORM 层 SQL 注入 | 用参数化查询 API |
| `WEAK_MESSAGE_DIGEST_MD5` / `_SHA1` | 弱哈希算法 | 敏感场景用 SHA-256+；密码用 BCrypt/PBKDF2/Argon2 |
| `CIPHER_INTEGRITY` / `ECB_MODE` / `PADDING_ORACLE` | 弱加密模式（ECB / 无完整性） | 用 `AES/GCM/NoPadding`，禁 ECB |
| `HARD_CODE_PASSWORD` / `HARD_CODE_KEY` | 硬编码口令/密钥 | 从环境变量/配置中心/KMS 读取 |
| `PREDICTABLE_RANDOM` | 用 `java.util.Random` 做安全用途 | 用 `SecureRandom` |
| `PATH_TRAVERSAL_IN` / `_OUT` | 路径穿越（外部输入拼路径） | 规范化路径并校验在允许根目录内（`Path.normalize()` + `startsWith`），拒绝 `..` |
| `XXE_SAXPARSER` / `_DOCUMENT` / `_XMLSTREAMREADER` | XML 外部实体注入 | 禁用外部实体：`setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)` |
| `URLCONNECTION_SSRF_FD` / `SSRF` | 服务端请求伪造（外部输入作 URL） | 白名单校验目标 host，禁内网地址段 |
| `COMMAND_INJECTION` | 命令注入（外部输入进 `Runtime.exec`） | 避免拼接命令，用参数数组形式并白名单校验 |
| `LDAP_INJECTION` / `XPATH_INJECTION` | LDAP / XPath 注入 | 对特殊字符转义或参数化 |
| `COOKIE_USAGE` / `INSECURE_COOKIE` / `HTTPONLY_COOKIE` | Cookie 缺安全属性 | 设 `Secure` + `HttpOnly` + `SameSite` |
| `TRUST_BOUNDARY_VIOLATION` | 未净化的外部数据进 session | 校验/净化后再存 |
| `OBJECT_DESERIALIZATION` | 反序列化不可信数据（RCE 入口） | 用白名单 `ObjectInputFilter`（JDK 9+）；禁止 `ObjectInputStream.readObject()` 直读外部输入 |
| `XSS_REQUEST_WRAPPER` / `XSS_SERVLET` | 反射型/存储型 XSS（输出未转义） | 输出编码（`HtmlUtils.htmlEscape` / OWASP Java Encoder）；CSP 头 |
| `CRLF_INJECTION_LOGS` | CRLF 注入日志（日志伪造/劫持） | 过滤 `\r\n` 或用日志框架的结构化字段参数化 |

## 四、SpotBugs 常见坑

- **必须先编译**：SpotBugs 分析 `target/classes`，未编译或编译产物过期会漏报/误报——门禁流程务必 `compile` 后立即扫描。
- **依赖 jar 需在 classpath**：SpotBugs 分析第三方类型时需能加载这些类。包装工程**不做编译**（仅 `spotbugs:spotbugs`），须从被检项目 pom 复制 `<dependencies>` 到包装 pom，否则报告 `<Errors missingClasses='N'>`，影响数据流分析精度。安全模式类检查（SQL 注入、弱加密等）基于 AST 模式匹配，不依赖类型解析，仍正常工作。详见 `01-setup.md` 第三节。
- **effort/threshold**：`effort=Max` + `threshold=Low` 报得最全，门禁再按 rank 过滤；生产 CI 可调 `threshold=Medium` 降噪。

## 五、工具层未覆盖的人工核查项

以下问题 PMD/SpotBugs 均不检测，需在门禁流程中人工核查：

- **线程池生命周期**：静态 `ExecutorService` 字段须显式 `shutdown()`/`shutdownNow()`，或交由 Spring 等容器托管。工具只检测"怎么创建"，不检测"怎么销毁"。
