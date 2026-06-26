# 命令示例

本章节汇总所有常用命令，便于快速查阅。

## Maven 命令

### 依赖树查看

```bash
# 查看完整依赖树
mvn dependency:tree

# 查看特定依赖
mvn dependency:tree -Dincludes=com.example:*

# 排除特定依赖
mvn dependency:tree -DexcludeTransitive

# 指定作用域过滤
mvn dependency:tree -Dscope=compile

# 详细输出（显示冲突）
mvn dependency:tree -Dverbose=true
```

### 依赖分析

```bash
# 查看依赖分析报告
mvn dependency:analyze

# 生成 HTML 报告（包含未声明的传递依赖）
mvn dependency:analyze-report
```

### 版本检查与漏洞扫描

```bash
# 检查可直接升级的依赖
mvn versions:display-dependency-updates

# 检查插件可用更新
mvn versions:display-plugin-updates

# OWASP Dependency-Check 扫描
mvn org.owasp:dependency-check-maven:check

# 生成漏洞报告
mvn org.owasp:dependency-check-maven:aggregate
```

## Gradle 命令

### 依赖树查看

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
```

### 版本检查

```bash
# 检查可用依赖更新
./gradlew dependencyUpdates

# 列出所有配置
./gradlew dependencies --configuration compileClasspath
```

## JAR 内嵌依赖检测

### 基础检测命令

```bash
# 查看 JAR 内容结构
jar tf app.jar | grep -E "META-INF|maven"

# 解压查看 pom.xml
unzip -p app.jar META-INF/maven/*/pom.xml

# 使用 jdeps 列出依赖（需要 JDK 8+）
jdeps -s app.jar
jdeps --list-deps app.jar

# 使用 procyon 反编译查看实际类（可选）
procyon -jar app.jar

# 查看 MANIFEST.MF 中的 Class-Path
unzip -p app.jar META-INF/MANIFEST.MF
```

### Spring Boot fat JAR

```bash
# 查看 Spring Boot JAR 结构
jar tf app.jar | grep BOOT-INF

# 查看内嵌依赖
jar tf app.jar | grep BOOT-INF/lib

# 解压查看
unzip -p app.jar BOOT-INF/lib/*.jar | head -5
```

### shaded JAR 分析

```bash
# 查看是否包含其他 JAR
jar tf app.jar | grep "\.jar$"

# 查看 Maven 元数据
jar tf app.jar | grep "META-INF/maven"

# 使用 jdeps 分析依赖
jdeps -R app.jar
```

## 扫描工具命令

### OSV Scanner

```bash
# 扫描目录
osv-scanner -r /path/to/project

# 扫描 Maven pom.xml
osv-scanner -L /path/to/project/pom.xml

# 扫描多个 lockfile
osv-scanner -L pom.xml -L build.gradle.lockfile

# JSON 输出
osv-scanner -r . --json > results.json

# 静默模式（仅显示漏洞）
osv-scanner -r . --quiet

# 排除目录
osv-scanner -r . --exclude /path/to/vendor
```

### Grype

```bash
# 扫描 JAR 文件
grype file:/path/to/app.jar

# 扫描 Docker 镜像
grype docker:myimage:latest

# JSON 输出
grype file:/path/to/app.jar -o json

# 指定数据库源
grype file:/path/to/app.jar --db ca-certs
```

### Trivy

```bash
# 扫描目录
trivy fs /path/to/project

# 扫描 JAR
trivy fs --format cyclonedx /path/to/app.jar

# 扫描 Docker 镜像
trivy image myimage:latest

# 按严重级别过滤
trivy fs --severity CRITICAL,HIGH /path/to/project

# JSON 输出
trivy fs --format json /path/to/project > results.json
```

## 快速修复命令

### Maven

```bash
# 一键检查可升级依赖
mvn versions:display-dependency-updates

# 生成详细依赖分析
mvn dependency:tree -Dverbose=true
```

### Gradle

```bash
# 检查可用更新
./gradlew dependencyUpdates

# 查看运行时依赖
./gradlew dependencies --configuration runtimeClasspath
```