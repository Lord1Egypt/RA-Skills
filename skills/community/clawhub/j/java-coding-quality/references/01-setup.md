# 01 · 接入与环境搭建

本文给出**零侵入包装工程**的完整落地模板（已在 Maven 3.6.3 + PMD 7.14.0 + SpotBugs 4.9.6 实跑验证），以及持久化、Gradle 配置。

## 一、零侵入 `.qualitygate/` 结构

在**被检项目根目录**下建：

```
<project-root>/
├── pom.xml                      # 项目自身 pom，全程零改动
├── src/main/java/...            # 被检源码
├── target/classes/...          # SpotBugs 分析的字节码（需先编译）
└── .qualitygate/                # 本技能生成，写入 .gitignore
    ├── pmd-pom.xml              # PMD 包装工程
    ├── spotbugs-pom.xml         # SpotBugs 包装工程
    └── pmd7-ruleset.xml # 从技能 assets/ 拷入
```

把 `.qualitygate/` 追加到项目 `.gitignore`（仅此一行改动，不动 pom）：

```bash
# bash / Git Bash（推荐，跨平台一致）
echo ".qualitygate/" >> .gitignore
```

> Windows PowerShell 5.1 的 `>>` 重定向默认写 UTF-16，会导致 git 无法解析 `.gitignore`。PowerShell 下改用：
> ```powershell
> Add-Content -Path .gitignore -Value '.qualitygate/' -Encoding UTF8
> ```

> 包装工程用 `${project.basedir}` 指向 `.qualitygate/` 自身目录；因此 `sourceDirectory` / classes 需用**相对上跳** `../` 指回被检项目。下方模板里已按「包装 pom 放在 `.qualitygate/` 内」写好路径。

## 二、PMD 包装 pom（`.qualitygate/pmd-pom.xml`）

PMD 7 解析**源码 AST，无需编译**。`packaging` 必须是 `jar`（`pom` 打包会导致插件跳过源码目录）。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example.qualitygate</groupId>
    <artifactId>qualitygate-pmd</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <!-- 与被检项目一致，探测得到的 targetJdk 填这里 -->
        <maven.compiler.release>17</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <build>
        <!-- 包装 pom 在 .qualitygate/ 内，上跳一级指向被检项目源码 -->
        <sourceDirectory>${project.basedir}/../src/main/java</sourceDirectory>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-pmd-plugin</artifactId>
                <version>3.27.0</version>   <!-- 默认内核 PMD 7.14.0 -->
                <configuration>
                    <rulesets>
                        <ruleset>${project.basedir}/pmd7-ruleset.xml</ruleset>
                    </rulesets>
                    <printFailingErrors>true</printFailingErrors>
                    <failOnViolation>true</failOnViolation>
                    <!-- 单文件解析失败不中断整体扫描（容错） -->
                    <skipPmdError>true</skipPmdError>
                    <targetJdk>${maven.compiler.release}</targetJdk>
                    <format>xml</format>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

**运行**（在被检项目根目录执行）：

```
# 只出报告不失败：pmd:pmd；要门禁失败用 pmd:check
mvn -f .qualitygate/pmd-pom.xml org.apache.maven.plugins:maven-pmd-plugin:3.27.0:pmd
```

- 报告输出：`.qualitygate/target/pmd.xml`（`format=xml`，可被程序解析）；同时生成 `target/reports/pmd.html` 便于人读。
- `pmd:check` 会在有违规时以非 0 退出（门禁失败）；`pmd:pmd` 只产报告。门禁循环里用 `pmd:pmd` 拿全量报告，自行按严重级判断更灵活。
- **auxclasspath 精度说明**：PMD 包装 pom 无 `<dependencies>`，依赖类型解析的规则（`CloseResource`、`CompareObjectsWithEquals` 等）在引用第三方类型的代码上精度可能下降（无法确定某类型是否 `Closeable`/`AutoCloseable`）。如需提升精度，可从被检项目 pom 复制 `<dependencies>` 到 PMD 包装 pom（与 SpotBugs 包装 pom 同理）。多数内置规则基于 AST 模式匹配，不依赖类型解析，仍正常工作。

## 三、SpotBugs 包装 pom（`.qualitygate/spotbugs-pom.xml`）

SpotBugs 分析**字节码，必须先编译**。正确流程是：**被检项目自行 `mvn compile`（依赖完整）→ 包装工程只分析已编译的字节码，不自行编译**。

> ⚠️ **关键**：包装 pom **不设 `sourceDirectory`、不做 `compile`**——否则包装工程缺项目 `<dependencies>`，含第三方依赖（slf4j / Spring 等）的项目必然 `BUILD FAILURE`（`程序包 xxx 不存在`）。包装 pom 的唯一职责是配置 SpotBugs + FindSecBugs 并指向被检项目的 `target/classes`。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example.qualitygate</groupId>
    <artifactId>qualitygate-spotbugs</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>   <!-- pom：不做编译，只跑 spotbugs:spotbugs -->

    <properties>
        <maven.compiler.release>17</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <!-- Agent 操作：从被检项目 pom.xml 复制 <dependencies>（compile + provided 作用域）至此。
         使 SpotBugs 能解析第三方类型，减少 missingClasses 误报。
         项目无第三方依赖时可省略此段。 -->
    <dependencies>
        <!-- 示例（按实际项目 pom 填入）：
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>1.7.36</version>
        </dependency>
        -->
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>com.github.spotbugs</groupId>
                <artifactId>spotbugs-maven-plugin</artifactId>
                <version>4.9.6.0</version>
                <configuration>
                    <effort>Max</effort>       <!-- 最大分析深度 -->
                    <threshold>Low</threshold> <!-- 报出 Low 及以上，门禁自筛 -->
                    <xmlOutput>true</xmlOutput>
                    <!-- 分析被检项目已编译的字节码（项目须先 mvn compile） -->
                    <classFilesDirectory>${project.basedir}/../target/classes</classFilesDirectory>
                    <plugins>
                        <plugin>
                            <groupId>com.h3xstream.findsecbugs</groupId>
                            <artifactId>findsecbugs-plugin</artifactId>
                            <version>1.14.0</version>
                        </plugin>
                    </plugins>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

**运行**（先编译被检项目，再用包装工程分析）：

```bash
# 1. 被检项目自行编译（依赖完整，编译产物在 target/classes）
mvn compile

# 2. 包装工程只分析，不编译
mvn -f .qualitygate/spotbugs-pom.xml com.github.spotbugs:spotbugs-maven-plugin:4.9.6.0:spotbugs
```

- 报告输出：`.qualitygate/target/spotbugsXml.xml`（`xmlOutput=true`）。根节点含 `<Plugin id='com.h3xstream.findsecbugs' enabled='true'>` 即证明 FindSecBugs 已挂载。
- `spotbugs:spotbugs` 只产报告；`spotbugs:check` 有 bug 时失败。门禁循环用 `spotbugs:spotbugs` 拿全量报告。
- 报告尾部 `<FindBugsSummary total_bugs='N' priority_1/2/3=.../>`：priority_1 是最高危（SpotBugs 内部数值，与 rank 不同，分级换算见 `04-fix-workflow.md`）。
- **auxclasspath 精度说明**：包装 pom 的 `<dependencies>` 须从被检项目 pom 复制（compile + provided 作用域），使 SpotBugs 能加载第三方类做数据流分析。若依赖未复制，SpotBugs 报告 `<Errors missingClasses='N'>`，部分数据流检查（NP_ 系列）精度下降，但安全模式类检查（SQL 注入、弱加密等）仍正常工作。

## 四、持久化进项目 pom（询问用户同意后）

扫描通过一次后，若用户同意持久化（供团队 / CI 共享），把插件写入**项目自身 pom** 的 `<build><plugins>`。此时 ruleset 建议放到项目 `config/pmd/` 下并纳入版本控制：

```xml
<!-- 项目 pom：PMD -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-pmd-plugin</artifactId>
    <version>3.27.0</version>
    <configuration>
        <rulesets><ruleset>config/pmd/pmd7-ruleset.xml</ruleset></rulesets>
        <printFailingErrors>true</printFailingErrors>
        <skipPmdError>true</skipPmdError>
    </configuration>
    <executions>
        <execution><phase>verify</phase><goals><goal>check</goal></goals></execution>
    </executions>
</plugin>
<!-- 项目 pom：SpotBugs + FindSecBugs -->
<plugin>
    <groupId>com.github.spotbugs</groupId>
    <artifactId>spotbugs-maven-plugin</artifactId>
    <version>4.9.6.0</version>
    <configuration>
        <effort>Max</effort><threshold>Low</threshold>
        <plugins>
            <plugin>
                <groupId>com.h3xstream.findsecbugs</groupId>
                <artifactId>findsecbugs-plugin</artifactId>
                <version>1.14.0</version>
            </plugin>
        </plugins>
    </configuration>
    <executions>
        <execution><phase>verify</phase><goals><goal>check</goal></goals></execution>
    </executions>
</plugin>
```

持久化后 `mvn verify` 即触发门禁，CI 直接复用。持久化 = **改动项目 pom**，务必先经用户明确同意。

## 五、Gradle 等价配置（简要）

被检项目为 Gradle 时，零侵入较难（Gradle 无等价「包装工程」惯例），推荐直接在 `build.gradle` 增插件（相当于持久化路径，需用户同意）：

```groovy
plugins {
    id 'pmd'
    id 'com.github.spotbugs' version '6.0.26'
}
pmd {
    toolVersion = '7.14.0'
    ruleSetFiles = files('config/pmd/pmd7-ruleset.xml')
    ruleSets = []   // 清空默认规则集，只用自带的
    ignoreFailures = false
}
dependencies {
    spotbugsPlugins 'com.h3xstream.findsecbugs:findsecbugs-plugin:1.14.0'
}
spotbugs { effort = 'max'; reportLevel = 'low' }
```

运行：`gradle pmdMain spotbugsMain`；报告在 `build/reports/pmd/` 与 `build/reports/spotbugs/`。

## 六、多模块 Maven 工程

聚合工程（multi-module）下 `../src/main/java` 的单模块路径假设不成立。适配方式：

1. **PMD**：包装 pom 的 `sourceDirectory` 改为聚合根的各模块源码目录列表（`<sourceDirectories>` 复数形式），或逐模块扫描：
   ```xml
   <sourceDirectories>
       <directory>${project.basedir}/../module-a/src/main/java</directory>
       <directory>${project.basedir}/../module-b/src/main/java</directory>
   </sourceDirectories>
   ```
2. **SpotBugs**：逐模块 `mvn compile` 后，`classFilesDirectory` 逐模块指向各自的 `target/classes`，或用聚合工程的 `target/classes`（需先 `mvn compile` 从聚合根触发全量编译）。
3. **推荐**：多模块工程优先走持久化路径（插件写入聚合 pom `<pluginManagement>`），各子模块继承配置，比零侵入包装更可靠。

## 七、适用边界声明

| 场景 | 适配情况 | 说明 |
|---|---|---|
| 单模块 Maven（Spring Boot 等） | ✅ 完全适配 | 默认场景，模板直接可用 |
| 多模块 Maven 聚合工程 | ⚠️ 需调整 | 见第六节，或优先持久化 |
| Gradle（Groovy DSL） | ⚠️ 降级 | 放弃零侵入，仅持久化路径（第五节） |
| Gradle（Kotlin DSL） | ❌ 未覆盖 | 需用户自行翻译 Groovy 配置 |
| 测试代码（`src/test/java`） | ❌ 不扫描 | 仅扫 `src/main/java`；测试代码质量另由 CI 规则覆盖。如需扫描测试代码，在包装 pom 增加 `testSourceDirectory`（PMD）或 `testClassFilesDirectory`（SpotBugs） |
