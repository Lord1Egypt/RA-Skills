# 漏洞扫描工具

以下工具可作为辅助，但必须验证其结果：

## 工具对比

| 工具 | 支持的构建工具 | 说明 |
|------|---------------|------|
| [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/) | Maven, Gradle | 支持 CI/CD 集成 |
| [OSV Scanner](https://github.com/google/osv-scanner) | Maven, Gradle, JAR | 基于 OSV 数据库 |
| [Grype](https://github.com/anchore/grype) | JAR, Docker 镜像 | 支持多种语言 |
| [Trivy](https://aquasecurity.github.io/trivy/) | JAR, Gradle lockfile, Docker 镜像 | 支持多种语言和基础设施 |
| [Nancy](https://sonatype.github.io/nancy/) | Maven, Gradle | Sonatype 开源版本 |
| [renovate](https://github.com/renovatebot/renovate) | Maven, Gradle | 自动更新依赖 |

## OSV Scanner

OSV（Open Source Vulnerabilities）提供免费 API，可用于查询漏洞：

```bash
# 扫描当前目录（递归）
osv-scanner -r /path/to/project

# 扫描指定 Maven pom.xml
osv-scanner -L /path/to/project/pom.xml

# 扫描多个 lockfile
osv-scanner -L pom.xml -L build.gradle.lockfile

# JSON 输出便于后续处理
osv-scanner -r . --json > results.json

# 仅显示漏洞信息，不显示详情
osv-scanner -r . --quiet

# 排除特定目录（如 node_modules, vendor）
osv-scanner -r . --exclude /path/to/vendor

# 直接调用 API 查询单个包
curl -X POST https://api.osv.dev/v1/query -d \
  '{"package":{"name":"org.apache.commons:commons-lang3","version":"3.12.0"}}'
```

## Grype

```bash
# 扫描 JAR 文件
grype file:/path/to/app.jar

# 扫描 Docker 镜像
grype docker:myimage:latest

# 指定输出格式
grype file:/path/to/app.jar -o json

# 指定漏洞数据库源
grype file:/path/to/app.jar --db ca-certs
```

## Trivy

```bash
# 扫描目录
trivy fs /path/to/project

# 扫描 JAR
trivy fs --format cyclonedx /path/to/app.jar

# 扫描 Docker 镜像
trivy image myimage:latest

# 指定严重级别过滤
trivy fs --severity CRITICAL,HIGH /path/to/project

# 输出 JSON 格式
trivy fs --format json /path/to/project > results.json
```

## OWASP Dependency-Check

```bash
# Maven 集成
mvn org.owasp:dependency-check-maven:check

# 生成报告
mvn org.owasp:dependency-check-maven:aggregate

# 指定项目类型
mvn org.owasp:dependency-check-maven:check -DassemblyName=myapp

# 仅扫描特定依赖
mvn org.owasp:dependency-check-maven:check -DdependsOn=runtime
```

## 使用建议

1. **交叉验证**：不要依赖单一工具的结果，使用 2-3 种工具交叉验证
2. **版本确认**：始终使用 dependency:tree 或 lockfile 确认实际版本
3. **数据库更新**：定期更新漏洞数据库，确保最新 CVE 被覆盖
4. **误报处理**：扫描器结果只是线索，需要人工核实受影响版本范围