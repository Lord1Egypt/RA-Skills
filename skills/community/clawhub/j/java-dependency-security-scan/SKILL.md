---
name: java-dependency-security-scan
description: 用于分析 Java、Maven 或 Spring 生态项目的依赖安全风险。当用户要求扫描依赖漏洞、核实某个依赖版本是否受影响、分析传递依赖、检查第三方 JAR 内嵌依赖、审阅 CVE 影响范围，或生成包含修复建议的依赖安全报告时使用。

## 适用范围

本 Skill 聚焦 Java 生态（Maven/Gradle）的依赖安全分析。其他语言项目可复用相同的漏洞分析方法，但需调整：
- 依赖获取命令（npm list, pip freeze 等）
- 锁文件格式（package-lock.json, Pipfile.lock 等）
- 漏洞数据源和 API 接口

---

## 快速开始

当用户提出以下需求时，使用本 Skill：

| 场景 | 示例 |
|------|------|
| 扫描项目依赖漏洞 | "扫描我的 Spring Boot 项目依赖漏洞" |
| 核实特定依赖 | "log4j-core 2.14.1 是否有漏洞？" |
| 分析 CVE 影响 | "CVE-2021-44228 对我的项目有什么影响？" |
| 检查传递依赖 | "分析项目中 commons-lang3 的依赖路径" |
| 检查 JAR 内嵌依赖 | "分析这个第三方 JAR 包里的依赖" |
| 生成安全报告 | "生成依赖安全扫描报告" |

---

## 核心工作流程

```
收集证据 → 界定范围 → 匹配漏洞 → 输出报告
```

### 1. 收集证据（按优先级）

| 优先级 | 证据类型 | 说明 |
|--------|----------|------|
| 1 | lockfile | gradle.lockfile、libs.versions.toml |
| 2 | dependency:tree | mvn dependency:tree / gradlew dependencies |
| 3 | 构建文件 | pom.xml / build.gradle 声明 |
| 4 | 用户输入 | 依赖清单、扫描报告 |

### 2. 界定扫描范围

**默认扫描**：
- Maven: `compile`、`runtime` scope
- Gradle: `runtimeClasspath`、`implementation` 配置
- 第三方 JAR 中实际携带的内嵌依赖

**默认排除**：
- `test`、`testImplementation` 等测试依赖
- `provided`、`compileOnly` 等容器提供依赖

### 3. 匹配漏洞

确认漏洞需同时满足：
- ✅ 依赖坐标明确（groupId:artifactId:version）
- ✅ 版本落入 CVE 公告的受影响范围
- ✅ 运行时实际生效（非被覆盖/排除）

### 4. 输出报告

按以下结构输出：
1. **扫描概况**：项目信息、依赖数量、漏洞统计
2. **漏洞明细**：按严重级别分组，包含 CVE、修复版本
3. **修复方案**：优先级排序的具体修复建议
4. **剩余风险**：未验证的假设和不确定性

---

## 关键原则

- **先收集证据，再下结论**：优先使用 lockfile 和 dependency:tree
- **双重验证**：扫描器结果只是线索，需人工核实版本和受影响范围
- **明确不确定性**：无法确认的信息要标注"需要验证"或"证据不足"
- **关注运行时**：默认只关注实际进入运行时类路径的依赖

---

## 目录

1. [执行原则与环境](./references/01-principles.md) - 证据权重、漏洞匹配标签、严重级别
2. [Maven 项目分析](./references/02-maven.md) - Maven 依赖树分析、scope 对照、传递依赖机制
3. [Gradle 项目分析](./references/03-gradle.md) - Gradle 依赖分析、配置对照、版本目录
4. [漏洞扫描工具](./references/04-tools.md) - OWASP DC、OSV、Grype、Trivy 等工具使用
5. [命令示例](./references/05-commands.md) - 常用命令速查手册
6. [输出与修复模板](./references/06-output.md) - 报告模板、修复代码示例
7. [参考与常见问题](./references/07-reference.md) - 速查表、FAQ、参考链接