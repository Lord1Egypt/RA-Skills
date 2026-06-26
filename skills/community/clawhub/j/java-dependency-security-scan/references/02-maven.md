# Maven 项目分析

## 支持的 Maven 项目类型

- 项目类型：标准 Maven 项目、多模块项目
- 依赖声明：`pom.xml`
- 传递依赖还原：`mvn dependency:tree`
- 锁文件：不适用（Maven 每次构建重新解析）

## Maven Scope 对照表

| Maven Scope | 运行时生效 | 说明 |
|-------------|-----------|------|
| compile | 是 | 默认作用域 |
| runtime | 是 | 编译不需要，运行时需要 |
| provided | 否 | 通常由运行容器提供 |
| test | 否 | 仅测试时使用 |
| import | 是 | BOM 导入专用 |

## 工作流程

### 1. 收集依赖证据

优先按以下顺序建立依赖事实：

1. 根目录和各模块的 `pom.xml`
2. 父 POM 与 `dependencyManagement`
3. `mvn dependency:tree`
4. 第三方 JAR 中的 Maven 元数据
5. 用户提供的依赖清单、扫描报告或截图

### 2. 收集证据规则

- 读取根 POM 和模块 POM，识别直接依赖、模块边界、作用域和打包方式。
- 如果存在父 POM 或 BOM，继续解析继承关系和统一版本覆盖。
- 如果 Maven 可用且项目可解析，优先运行依赖树来恢复传递依赖。
- 如果用户提供第三方 JAR，检查其中的 `META-INF/maven/**/pom.xml`、`pom.properties` 和其他可识别的内嵌依赖线索。
- 对 shaded、fat jar、vendor bundle 这类产物，区分"项目声明的依赖"与"产物实际携带的依赖"。
- 如果某些模块无法构建、版本由私服控制、或依赖关系不完整，明确标记为"证据不足"或"需要验证"。

### 3. 界定扫描范围

默认扫描以下内容：

- Maven：`compile`、`runtime`
- 能从项目或构件元数据中还原出的传递依赖
- 第三方 JAR 中实际随包分发的内嵌依赖

默认不扫描以下内容，除非用户明确要求：

- Maven：`test`
- 一般由运行容器提供的 `provided`
- 明显属于项目内部自研模块且当前任务只关注第三方组件风险的部分

只要做了排除，就要说明原因。不要静默过滤关键依赖。

### 4. Maven 传递依赖机制

分析传递依赖时，参考 [Maven 官方文档](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)。

特别注意以下机制：

- `nearest definition`：同一组件出现多个版本时，默认采用离当前项目更近的定义；如果深度相同，则通常以先声明者为准。
- `dependencyManagement` / BOM：父 POM、BOM 或当前 POM 中的版本管理可能覆盖传递依赖的实际生效版本。
- `scope` 传播：`compile`、`runtime`、`provided`、`test` 的传递规则不同，某些依赖虽然出现在树中，但未必进入运行时类路径。
- `optional`：上游标记为可选的依赖，不会自动作为下游项目的传递依赖生效。
- `exclusion`：上层依赖可能显式排除了某些组件，不能只看上游库的原始依赖关系。

在判断"项目是否受某个传递依赖漏洞影响"时，不要只根据扫描器列出的树形路径下结论；要结合有效 POM、版本覆盖、作用域和排除规则确认最终生效结果。

## Maven 命令

```bash
# 查看完整依赖树
mvn dependency:tree

# 查看特定依赖
mvn dependency:tree -Dincludes=com.example:*

# 查看依赖分析报告
mvn dependency:analyze

# 查看依赖分析报告（包含未声明的传递依赖）
mvn dependency:analyze-report

# 排除特定依赖
mvn dependency:tree -DexcludeTransitive

# 指定作用域过滤
mvn dependency:tree -Dscope=compile

# 检查可直接升级的依赖
mvn versions:display-dependency-updates

# 检查插件可用更新
mvn versions:display-plugin-updates

# 扫描已知漏洞（需提前配置）
mvn org.owasp:dependency-check-maven:check

# 生成详细依赖分析报告
mvn dependency:tree -Dverbose=true
```

## 漏洞来源

尽量基于权威来源下结论：

- 优先使用 [CVE 官方数据库](https://www.cve.org/) 或厂商/项目官方安全公告。
- 对 Spring、Spring Boot、Spring Security 及相关生态组件，必须同时查阅 [Spring Security Advisories](https://spring.io/security) 或对应官方公告。
- 只有当本地依赖证据与权威公告中的受影响范围能够互相支撑时，才能写成"已确认受影响"。
- 如果多个来源结论冲突，写清冲突点，不要自行消解成单一结论。
- 不要只根据 CVSS 分数判断实际风险；结合项目暴露面、调用路径和运行场景说明影响。