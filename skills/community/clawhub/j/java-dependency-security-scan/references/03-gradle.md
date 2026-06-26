# Gradle 项目分析

## 支持的 Gradle 项目类型

- 项目类型：标准 Gradle 项目、多模块项目、Android 项目
- 依赖声明：`build.gradle` / `build.gradle.kts`
- 传递依赖还原：`./gradlew dependencies` 或 `./gradlew :module:dependencies`
- 锁文件：`gradle.lockfile`、`libs.versions.toml`（Gradle 8+）

## Gradle Configuration 对照表

| Gradle Configuration | 运行时生效 | 说明 |
|---------------------|-----------|------|
| api | 是 | 编译当前模块并传递（类似旧的 compile） |
| implementation | 是 | 仅编译当前模块，不传递（Gradle 3.0+ 替代 compile） |
| runtimeOnly | 是 | 仅运行时需要，编译时不需要 |
| compileOnly | 否 | 仅编译时需要，不进入运行时类路径 |
| testImplementation | 否 | 测试专用 |
| testRuntimeOnly | 否 | 仅测试运行时需要 |

## 工作流程

### 1. 收集依赖证据

优先按以下顺序建立依赖事实：

1. 根目录和各子项目的 `build.gradle` / `build.gradle.kts`
2. `settings.gradle` / `settings.gradle.kts`（模块配置）
3. `gradle.properties`（属性配置）
4. `libs.versions.toml`（Gradle 8+ 版本目录）
5. `gradle.lockfile`（依赖锁文件）
6. `./gradlew dependencies --configuration runtimeClasspath`
7. 第三方 JAR 中的 Maven 元数据

### 2. 收集证据规则

- 读取根构建脚本和各子项目构建脚本，识别直接依赖、配置（`implementation`、`api`、`compileOnly`、`runtimeOnly`等）、子项目名称。
- 如果使用版本目录（`libs.versions.toml`），解析统一版本定义。
- 如果存在依赖锁文件（`gradle.lockfile`），优先使用锁文件中的精确版本，因为它是构建时实际解析的结果。
- 使用 `--configuration` 参数指定要检查的配置，如 `runtimeClasspath`、`implementation` 等。
- 对 shaded、fat jar、vendor bundle 这类产物，区分"项目声明的依赖"与"产物实际携带的依赖"。

### 3. 界定扫描范围

默认扫描以下内容：

- Gradle：`runtimeClasspath`、`implementation`（运行时生效的配置）
- 能从项目或构件元数据中还原出的传递依赖
- 第三方 JAR 中实际随包分发的内嵌依赖

默认不扫描以下内容，除非用户明确要求：

- Gradle：`testImplementation`、`testRuntimeOnly`
- 一般由运行容器提供的 `compileOnly`
- 明显属于项目内部自研模块且当前任务只关注第三方组件风险的部分

只要做了排除，就要说明原因。不要静默过滤关键依赖。

### 4. Gradle 传递依赖机制

分析传递依赖时，参考 [Gradle 官方文档](https://docs.gradle.org/current/userguide/viewing_debugging_dependencies.html)。

特别注意以下机制：

- 版本目录（`libs.versions.toml`）：统一管理版本，可能覆盖传递依赖的版本。
- 依赖替换（`dependencySubstitution`）：通过版本插件或规则替换依赖。
- `implementation` vs `api`：使用 `implementation` 的依赖默认不传递，使用 `api` 的才会传递。
- `transitive`：可显式控制是否解析传递依赖。
- `exclude`：可显式排除特定传递依赖。

在判断"项目是否受某个传递依赖漏洞影响"时，不要只根据扫描器列出的树形路径下结论；要结合版本目录、版本覆盖、配置类型和排除规则确认最终生效结果。

## Gradle 命令

```bash
# 查看完整依赖树（所有配置）
./gradlew dependencies

# 查看特定模块的依赖树
./gradlew :module:dependencies

# 查看特定配置（如 runtimeClasspath）
./gradlew dependencies --configuration runtimeClasspath

# 查看特定配置的依赖树
./gradlew dependencies --configuration implementation

# 生成 HTML 报告（需要配置）
./gradlew htmlDependencyReport

# 查看特定依赖
./gradlew dependencies --configuration runtimeClasspath | grep commons-lang3

# 检查可用依赖更新
./gradlew dependencyUpdates

# 查看所有配置
./gradlew dependencies --configuration compileClasspath
```

## 混合项目

如果项目同时包含 Maven 和 Gradle 配置，需分别执行扫描并合并结果。