---
name: jar-conflict-detector
description: >
  This skill should be used when the user needs to detect JAR package conflicts,
  version inconsistencies, or known incompatible dependency pairs in a Spring Boot
  microservices project. Trigger phrases include: "检测 jar 包冲突", "依赖冲突分析",
  "dependency conflict", "jar 版本冲突", "pom 依赖检查", "排查 NoSuchMethodError",
  "Spring Boot 升级冲突", or any request involving Maven/Gradle dependency resolution
  issues in a Java/Spring Boot project.
---

# JAR 包冲突检测 Skill — Spring Boot 微服务

## 目的

To detect version conflicts, known incompatible dependency pairs, and duplicate JARs
in Spring Boot microservice projects (Maven or Gradle), and produce an actionable
conflict report with resolution suggestions.

## 触发场景

Use this skill when the user:
- Reports runtime errors such as `NoSuchMethodError`, `ClassNotFoundException`, `LinkageError`
- Asks to check or analyze JAR conflicts, version convergence, or dependency tree issues
- Is upgrading Spring Boot (e.g., 2.x → 3.x) and needs conflict validation
- Wants a dependency health check before CI/CD deployment
- Mentions Spring Cloud + Spring Boot version mismatch

## 工作流程

### Step 1 — 确认项目目录和构建工具

Ask the user for (or infer from context):
1. **Project root directory** — path to the Maven/Gradle project (containing `pom.xml` or `build.gradle`)
2. **Build tool** — auto-detected if not specified (`maven` | `gradle` | `auto`)
3. **Report format** — `html` (default, visual) | `txt` | `json` (for CI)
4. **Severity level** — `all` (default) | `warn` | `error`

For multi-module projects, always point to the **parent/root** directory so all sub-modules are scanned.

### Step 2 — 运行检测脚本

Run the bundled detection script:

```bash
python scripts/detect_conflicts.py \
  --project-dir <用户项目路径> \
  --output conflict-report.html \
  --mode auto \
  --level all
```

**Script capabilities:**
- Runs `mvn dependency:tree` (Maven) or `gradle dependencies` (Gradle) to get the full resolved dependency tree
- Falls back to static `pom.xml` parsing if Maven/Gradle CLI is unavailable
- Detects **version conflicts**: same `groupId:artifactId`, different versions across modules
- Detects **known incompatible pairs**: e.g., Spring Boot 3.x + Spring 5.x, dual SLF4J bindings
- Generates reports in HTML / TXT / JSON format

**Output files:**
- `conflict-report.html` — visual HTML report (default, recommended)
- `conflict-report.txt` — plain text for terminal review
- `conflict-report.json` — machine-readable for CI integration

### Step 3 — 解读结果并给出建议

After scanning, present results clearly:

1. **总结** — X 个 ERROR，Y 个 WARN，依赖总数
2. **逐条解读** — 对每个 ERROR 级冲突说明原因和影响
3. **给出修复方案** — 参考 `references/conflict_patterns.md` 提供具体 POM/Gradle 修改示例

For resolution guidance, load `references/conflict_patterns.md` which contains:
- Common conflict patterns and fixes
- Spring Boot / Spring Cloud / Hibernate version compatibility matrix
- SLF4J binding conflict resolution
- javax → jakarta migration guide
- Maven Enforcer plugin setup for CI enforcement

### Step 4 — 可选：生成修复建议 POM 片段

If the user wants specific fixes, generate the corresponding `dependencyManagement`
XML snippet or Gradle `resolutionStrategy` block inline in the reply.

## 输出格式指南

- **HTML 报告** — 默认推荐，适合人工审查，call `preview_url` or `open_result_view`
- **JSON 报告** — 适合 CI pipeline 解析，结合 `jq` 过滤 ERROR 级别
- **TXT 报告** — 适合终端快速查看

## 注意事项

- If `mvn`/`gradle` is not available on PATH, the script falls back to static POM parsing
  (less accurate — transitive dependencies won't be resolved). Inform the user.
- For **Spring Boot 3.x migration**, always check for `javax.*` → `jakarta.*` conflicts.
- For **multi-module projects**, run from the **root directory** with the parent `pom.xml`.
- Script exit code: `0` = no ERROR conflicts; `1` = at least one ERROR found (useful for CI gates).
- All Python stdlib only — no pip install required.
