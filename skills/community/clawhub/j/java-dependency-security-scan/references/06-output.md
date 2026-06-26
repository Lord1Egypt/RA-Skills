# 输出与修复模板

## 输出结构

除非用户明确要求其他格式，否则按以下结构输出。

### 1. 扫描概况

至少包含：

- 项目名或模块名
- 构建工具类型（Maven / Gradle / 混合）
- 扫描模块数
- 检查的依赖数量
- 已确认漏洞数量
- `需要验证` 数量
- 最高严重级别

### 2. 漏洞明细

按模块、依赖来源或风险等级分组列出。每条至少包含：

- 依赖坐标：`groupId:artifactId:version`
- 依赖来源：直接依赖、传递依赖、JAR 内嵌依赖
- 漏洞编号：CVE 或官方公告编号
- 严重级别
- 命中依据
- 修复版本或安全版本范围
- 结合项目上下文的简短影响说明

如果漏洞很多，先给摘要表，再补充重点说明。

### 3. 修复方案

每个已确认问题都要给出主要修复建议。优先顺序通常为：

1. 直接升级到安全版本
2. 排除有漏洞的传递依赖并显式引入安全版本
3. 通过 `dependencyManagement`（Maven）或 `dependencies`（Gradle）统一覆盖到安全版本
4. 如果漏洞仅存在于供应商 JAR 内嵌组件中且无法单独排除，建议升级或替换上层构件

给出升级建议时，提醒兼容性验证风险，尤其是：

- 主版本升级
- Spring Boot / Spring Cloud 组合升级
- Servlet 容器或 JDK 基线变化
- API/ABI 兼容性变化

### 4. 剩余风险与假设

列出所有尚未完全验证的点，例如：

- 传递依赖版本未能完整还原
- 私有制品缺少公开元数据
- JAR 内嵌内容无法完整枚举
- 结论依赖用户提供的片段式扫描结果

## Maven 修复模板

### 升级直接依赖

```xml
<dependency>
    <groupId>${groupId}</groupId>
    <artifactId>${artifactId}</artifactId>
    <version>${safeVersion}</version>
</dependency>
```

### 覆盖传递依赖版本

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>${groupId}</groupId>
            <artifactId>${artifactId}</artifactId>
            <version>${safeVersion}</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### 排除有漏洞的传递依赖

```xml
<dependency>
    <groupId>${parentGroupId}</groupId>
    <artifactId>${parentArtifactId}</artifactId>
    <version>${parentVersion}</version>
    <exclusions>
        <exclusion>
            <groupId>${vulnGroupId}</groupId>
            <artifactId>${vulnArtifactId}</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

## Gradle 修复模板

### 升级直接依赖

```groovy
// build.gradle.kts
implementation("org.apache.commons:commons-lang3:3.12.0")
```

### 强制指定版本（覆盖传递依赖）

```groovy
// build.gradle.kts
configurations.all {
    resolutionStrategy {
        force 'org.apache.commons:commons-lang3:3.12.0'
    }
}
```

或使用版本目录：

```groovy
// libs.versions.toml
[versions]
commons-lang3 = "3.12.0"

[libraries]
commons-lang3 = { group = "org.apache.commons", name = "commons-lang3", version.ref = "commons-lang3" }
```

### 排除传递依赖

```groovy
// build.gradle.kts
implementation("org.example:parent-lib:1.0.0") {
    exclude(group = "org.apache.commons", module = "commons-lang3")
}
```

## JAR 内嵌依赖修复

对于 shaded JAR 或 Spring Boot fat JAR 中的内嵌依赖问题：

### 方案一：升级上层构件

如果内嵌的漏洞组件来自父依赖，优先考虑升级父依赖到不含漏洞的版本。

### 方案二：替换为官方最小化依赖

如果父依赖无法升级，检查是否有更轻量的替代品，不含内嵌的有毒依赖。

### 方案三：重新打包

使用 Maven Shade 插件或 Gradle Shadow 插件重新打包，显式排除有问题的内嵌 JAR。

### 方案四：升级运行时

如果漏洞依赖特定 JDK 版本或容器版本，通过升级运行环境来规避。