# 02 · PMD 7 规则集

本文说明 `assets/pmd7-ruleset.xml`（规则集名 `Java Quality Ruleset (PMD 7)`）的设计、每条规则的来源与判定，以及高频告警的修复速查。所有规则已在 PMD 7.14.0 实跑验证命中。

## 一、设计原则

- **PMD 7 + 自研规则集**。
- 由两部分构成：① **PMD 7 内置规则引用 + 调参**（41 条，映射编码强制项）；② **XPath 3.1 自定义规则**（5 条，含 3 条 Spring 框架层反模式，补充内置未覆盖项）。
- **只收 AI 生成代码真实高频命中的强制项**；不收纯注释规约（ali-comment，AI 场景价值低）与需复杂数据流分析的规则（交给 SpotBugs 层）。
- `priority` 语义（与门禁分级对应，详见 `04-fix-workflow.md`）：**1=Blocker，2=Critical，3=Major，4/5=Minor**。

## 二、规则映射表

> 关键坑：PMD 7.14.0 中 category 归属与旧文档/snapshot 不同——`AvoidCatchingGenericException` 在 **design** 而非 errorprone；`ReplaceJavaUtilDate/Calendar` 在 7.14.0 **不存在**（已剔除）。下表为实跑核实的正确路径。

| 分类 | 规则 ID（category 路径） | priority | 命中场景 |
|---|---|---|---|
| 异常 | errorprone/`EmptyCatchBlock` | 1 | 空 catch 吞异常 |
| 异常 | design/`AvoidCatchingGenericException` | 2 | `catch (Exception/RuntimeException/Throwable)` |
| 异常 | errorprone/`ReturnFromFinallyBlock` | 1 | finally 中 return（吞原始异常） |
| 异常 | errorprone/`DoNotThrowExceptionInFinally` | 1 | finally 中 throw |
| 异常 | bestpractices/`PreserveStackTrace` | 2 | catch 后抛新异常丢原始栈 |
| 异常 | design/`AvoidThrowingRawExceptionTypes` | 3 | 抛裸 `RuntimeException`/`Exception` |
| 并发 | multithreading/`UnsynchronizedStaticFormatter` | 1 | 静态/共享 `SimpleDateFormat` 等 Format |
| 并发 | multithreading/`DontCallThreadRun` | 2 | 直接调 `thread.run()` 而非 `start()` |
| 并发 | multithreading/`DoubleCheckedLocking` | 1 | 未 volatile 的双重检查锁 |
| 并发 | multithreading/`AvoidThreadGroup` | 3 | 使用过时且非线程安全的 ThreadGroup |
| 金额 | errorprone/`AvoidDecimalLiteralsInBigDecimalConstructor` | 1 | `new BigDecimal(0.1)` 精度陷阱 |
| 常量 | errorprone/`AvoidDuplicateLiterals` | 3 | 重复字符串字面量应抽常量 |
| 常量 | errorprone/`AvoidLiteralsInIfCondition` | 3 | if 条件中的魔法值 |
| OOP | bestpractices/`MissingOverride` | 3 | 重写方法漏 `@Override`（降 Major：标注遗漏不应阻塞交付） |
| OOP | errorprone/`OverrideBothEqualsAndHashcode` | 1 | equals/hashCode 未成对重写 |
| OOP | errorprone/`CompareObjectsWithEquals` | 2 | 对象引用用 `==` 比较 |
| OOP | errorprone/`UseEqualsToCompareStrings` | 1 | 字符串用 `==`/`!=` 比较 |
| OOP | bestpractices/`LiteralsFirstInComparisons` | 2 | `str.equals("x")` 未把常量前置（NPE 风险） |
| OOP | errorprone/`MissingSerialVersionUID` | 3 | Serializable 类缺 serialVersionUID |
| OOP | bestpractices/`MethodReturnsInternalArray` | 3 | getter 直接返回内部数组 |
| OOP | bestpractices/`ArrayIsStoredDirectly` | 3 | 直接存储传入数组引用 |
| OOP | errorprone/`ReturnEmptyCollectionRatherThanNull` | 2 | 方法返回 null 而非空集合（NPE 高频根因） |
| 控制语句 | bestpractices/`NonExhaustiveSwitch` | 2 | switch 缺 default（sealed 穷尽除外） |
| 控制语句 | codestyle/`ControlStatementBraces` | 3 | if/for/while 缺大括号 |
| 资源 | errorprone/`CloseResource` | 1 | Connection/Statement/Stream 未关闭 |
| 命名 | codestyle/`ClassNamingConventions`（配命名正则） | 3 | 抽象类须 `Abstract/Base` 前缀、工具类 `Utils?/Helper` 后缀 |
| 命名 | codestyle/`MethodNamingConventions` | 3 | 方法名非 lowerCamelCase |
| 命名 | codestyle/`FieldNamingConventions` | 4 | 字段非 lowerCamelCase / 常量非 UPPER_SNAKE（`static final` mutable 对象如 ExecutorService 也可能触发，已降级 Minor） |
| 命名 | codestyle/`FormalParameterNamingConventions` | 4 | 形参名 |
| 命名 | codestyle/`LocalVariableNamingConventions` | 4 | 局部变量名 |
| 命名 | codestyle/`PackageCase` | 3 | 包名含大写 |
| 安全 | bestpractices/`AvoidUsingHardCodedIP` | 3 | 硬编码 IP |
| 安全 | bestpractices/`AvoidMessageDigestField` | 2 | `MessageDigest` 作共享字段（非线程安全） |
| 日志 | bestpractices/`SystemPrintln` | 3 | `System.out/err.print` 调试残留 |
| 日志 | bestpractices/`AvoidPrintStackTrace` | 3 | `e.printStackTrace()` 应换日志框架 |
| 日志 | bestpractices/`GuardLogStatement` | 4 | 日志调用前应检查级别（性能/安全） |
| 无用代码 | bestpractices/`UnusedLocalVariable`、`UnusedPrivateField`、`UnusedPrivateMethod` | 3 | 死代码 |
| 无用代码 | codestyle/`UnnecessaryImport` | 4 | 多余 import |
| 性能 | performance/`UseStringBufferForStringAppends` | 3 | 循环内字符串 `+=` 拼接应改 `StringBuilder` |

`ClassNamingConventions` 的命名风格 properties：

```xml
<property name="abstractClassPattern" value="(Abstract|Base)[A-Z][a-zA-Z0-9]*"/>
<property name="utilityClassPattern" value="[A-Z][a-zA-Z0-9]*(Utils?|Helper)"/>
```

## 三、XPath 自定义规则清单

内置规则未覆盖的特有强制项，用 XPath 3.1 自定义（`class="net.sourceforge.pmd.lang.rule.xpath.XPathRule"`）：

| 规则名 | priority | 判定逻辑 | 命中示例 |
|---|---|---|---|
| `AvoidExecutorsForThreadPool` | 1 | `MethodCall` 的 `@MethodName` 属 `newFixedThreadPool` 等 6 个工厂方法 **且** `TypeExpression/ClassType[@SimpleName='Executors']` | `Executors.newFixedThreadPool(10)` |
| `AvoidBooleanIsPrefixField` | 2 | 两个分支：(a) `FieldDeclaration` 中 `Boolean`/`boolean` 类型且变量名 `^is[A-Z]`；(b) `MethodDeclaration` 返回 `Boolean`(包装类型)、0 参数、方法名 `^is[A-Z]`。**不拦截 primitive boolean 的 `isXxx()`**（标准 JavaBeans 约定） | `private Boolean isDeleted;` / `public Boolean isDeleted()` |
| `TransactionalOnNonProxyableMethod` | 1 | `MethodDeclaration` 的 `ModifierList` 含 `@Transactional` 注解 **且** 方法是 `@Static`/`@Final`/`@Visibility='private'`（CGLIB/JDK 代理无法覆盖 → 事务静默失效） | `@Transactional private void insert()` |
| `TransactionalMissingRollbackFor` | 2 | 方法上 `@Transactional` 注解的 `AnnotationMemberList` 无 `rollbackFor`/`rollbackForClassName`（受检异常默认提交不回滚） | `@Transactional public void upload() throws IOException` |
| `AvoidDeprecatedListenableFuture` | 3 | `ClassType` 匹配 `org.springframework.util.concurrent.ListenableFuture`（Spring 6 / SpringBoot 3.x 已 `@Deprecated`） | `public ListenableFuture<String> sendAsync()` |

> **Spring 规则的取舍**：只收**单点 AST 可判、零误报**的（修饰符 / 注解参数 / 类型引用）；自调用失效、`@Async` 默认线程池、循环依赖等需跨方法/跨文件语义的陷阱**不收**（高误报损害门禁可信度，参考已移除的 `AvoidManualThreadCreation` 先例）。这些语义级陷阱由 **spring-boot-dev** 技能的 `references/12-pitfalls.md` 存量审查 checklist 覆盖（agent 用 ripgrep + 语言理解定位，非硬门禁）。

**踩坑记录**（维护时避免重蹈）：
- `AvoidBooleanIsPrefixField` 最初用 `pmd-java:typeIs('java.lang.Boolean')` 作用在 `FieldDeclaration` 上**不生效**——字段声明节点的类型需靠结构化子节点 `ClassType[@SimpleName='Boolean']` / `PrimitiveType[@Kind='boolean']` 匹配。
- `typeIs()` 在 `ConstructorCall/ClassType`（如 Thread）上工作正常，但对字段类型不可靠——**类型精确匹配优先在构造/方法调用节点用 `typeIs`，字段/变量声明用结构 + `@SimpleName`**。
- getter 匹配分支用 `ClassClass`（direct child）匹配 `MethodDeclaration` 的返回类型；用 `not(FormalParameters/FormalParameter)` 判断 0 参数。仅拦截 `Boolean`(包装类型) getter，不拦截 primitive `boolean isXxx()`（标准 JavaBeans）。若 PMD 版本升级后 AST 结构变化导致 getter 分支失效，规则仍不会误报（只是少报），不影响门禁安全性。
- **PMD 7 修饰符是属性不是子节点**：`MethodDeclaration` 通过 `ModifierOwner` 接口暴露 `@Static`/`@Final`/`@Visibility` XPath 属性（源自 `isStatic()`/`isFinal()`/`getVisibility()` 的 JavaBeans 命名）。**不要**找 `ModifierList/Modifier` 或 `ModifierList/Keyword` 子节点（不存在）。
- **`@Visibility` 枚举值是小写**：写 `@Visibility = 'private'`（不是 `'PRIVATE'`）。PMD 7 的枚举在 XPath 属性里以小写形式暴露。
- **注解参数节点名**：`AnnotationMemberList`（不是 `AnnotationArgumentList`）+ `MemberValuePair`（不是 `MemberReference`），`@Name` 属性是参数 key（如 `rollbackFor`）。
- **`TransactionalMissingRollbackFor` 须限定方法**：用 `//MethodDeclaration/ModifierList/Annotation` 而非 `//Annotation`，否则构造器/字段上的 `@Transactional`（无意义但合法）会误报。

## 四、高频告警 → 修复手法速查

只收 AI 生成代码真实会命中的。所有修复手法已内联，单装本技能即可闭环。

| 告警 | ✗ 反例 | ✓ 修复 |
|---|---|---|
| AvoidExecutorsForThreadPool | `Executors.newFixedThreadPool(10)` | `new ThreadPoolExecutor(核心,最大,keepAlive,单位,有界队列,拒绝策略)` |
| UnsynchronizedStaticFormatter | `static SimpleDateFormat SDF` | 换 `DateTimeFormatter`（线程安全）或 `ThreadLocal<SimpleDateFormat>` |
| AvoidDecimalLiteralsInBigDecimalConstructor | `new BigDecimal(0.1)` | `new BigDecimal("0.1")` 或 `BigDecimal.valueOf(0.1)` |
| EmptyCatchBlock | `catch (E e) {}` | 记日志或转译异常；确要忽略须注释说明 |
| AvoidCatchingGenericException | `catch (Exception e)` | 缩窄到具体异常类型分别处理 |
| ReturnFromFinallyBlock | `finally { return x; }` | 移除 finally 内 return，改在正常流程返回 |
| UseEqualsToCompareStrings | `a == b`（String） | `Objects.equals(a, b)` 或 `a.equals(b)` |
| LiteralsFirstInComparisons | `str.equals("x")` | `"x".equals(str)`（防 str 为 null） |
| CompareObjectsWithEquals | 对象 `==` | `equals()` / `Objects.equals` |
| NonExhaustiveSwitch | switch 无 default | 补 `default` 分支（或 sealed 穷尽所有子类型） |
| OverrideBothEqualsAndHashcode | 只重写 equals | 同时重写 hashCode（IDE 生成或 `Objects.hash`） |
| MissingSerialVersionUID | implements Serializable 无 UID | 加 `private static final long serialVersionUID = 1L;` |
| CloseResource | JDBC/Stream 未关 | try-with-resources |
| ReturnEmptyCollectionRatherThanNull | `return null;`（集合方法） | `return Collections.emptyList();` / `return List.of();` |
| SystemPrintln | `System.out.println(...)` | `log.info(...)` / `log.debug(...)`（用日志框架） |
| AvoidPrintStackTrace | `e.printStackTrace()` | `log.error("操作失败", e)`（用日志框架记录异常栈） |
| UseStringBufferForStringAppends | `s += "x"`（循环内） | `sb.append("x")`（用 `StringBuilder`） |
| AvoidBooleanIsPrefixField | `private Boolean isDeleted;` / `public Boolean isDeleted()` | 改 `deleted`；getter 改 `getDeleted()`。primitive `boolean isActive()` 不拦截 |
| AvoidMessageDigestField | `MessageDigest` 作字段 | 方法内局部创建，每次 `MessageDigest.getInstance("SHA-256")` |
| TransactionalOnNonProxyableMethod | `@Transactional private/static/final void method()` | 改为 `public` 非 `final` 非 `static`（AOP 代理要求） |
| TransactionalMissingRollbackFor | `@Transactional public void upload() throws IOException` | 加 `rollbackFor = Exception.class`（默认只回滚 RuntimeException） |
| AvoidDeprecatedListenableFuture | `public ListenableFuture<String> sendAsync()`（SpringBoot 3.x） | 改 `CompletableFuture<String>` |

## 五、规则集维护指引

### 5.1 新增一条内置规则
在对应分组下加 `<rule ref="category/java/<分类>.xml/<规则ID>"><priority>N</priority></rule>`。**务必先用本机 PMD 版本核实规则 ID 与 category 归属**（不同小版本会迁移分类）：
```
# 列出某分类全部规则做核对（bash/Git Bash）
mvn -f .qualitygate/pmd-pom.xml org.apache.maven.plugins:maven-pmd-plugin:3.27.0:pmd -X 2>&1 | grep "Rule"
# PowerShell 用 Select-String "Rule" 替换 grep
```
或查 https://docs.pmd-code.org/pmd-doc-7.14.0/pmd_rules_java.html （版本号对齐）。

### 5.2 新增一条 XPath 规则
1. 用 PMD 的 AST dumper 看目标代码的节点结构（PMD 7 的节点名与 6 不同，如 `MethodCall`/`ConstructorCall`/`ClassType`/`VariableId`）：
   ```
   pmd ast-dump --language java --file Target.java
   ```
2. 写 XPath，类型判断优先级：**构造/方法调用节点用 `pmd-java:typeIs('全限定名')`；字段/变量声明用结构匹配 `ClassType[@SimpleName='X']`**。
3. 加到规则集 XPath 段，带 `message`（中文含修复提示）、`priority`、`<example>`。
4. 在本地 fixture（`tests/fixtures/coding-quality-sample/`）加对应毒点，实跑确认命中再提交。

### 5.3 验证规则集无语法错误
任何改动后跑一次，PMD 会在启动时校验 ruleset；若某规则 ID 不存在或 XPath 语法错，会报 `rule validation error` 并列出问题规则：
```
mvn -f .qualitygate/pmd-pom.xml org.apache.maven.plugins:maven-pmd-plugin:3.27.0:pmd
```
