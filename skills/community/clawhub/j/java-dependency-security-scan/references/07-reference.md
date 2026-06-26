# 参考与常见问题

## Maven Scope 与 Gradle Configuration 对照

| Maven Scope | Gradle Configuration | 运行时生效 | 说明 |
|-------------|----------------------|-----------|------|
| compile | api, implementation | 是 | Gradle 3.0+ 推荐使用 implementation |
| runtime | runtimeOnly | 是 | - |
| provided | compileOnly | 否 | 通常由运行容器提供 |
| test | testImplementation, testRuntimeOnly | 否 | 仅测试时使用 |
| import | 不适用 | 是 | BOM 导入专用 |

## 证据权重速查

| 证据类型 | 权重 | 优先级 |
|---------|------|--------|
| lockfile | 最高 | 1st |
| dependency:tree 输出 | 高 | 2nd |
| pom.xml / build.gradle 声明 | 中 | 3rd |
| 用户提供的依赖清单 | 低 | 4th |

**原则**：优先使用 lockfile 和 dependency:tree 作为权威证据。

## 漏洞匹配标签

| 标签 | 含义 | 使用条件 |
|------|------|----------|
| 已确认 | 证据充分，影响关系成立 | groupId:artifactId:version 与受影响版本范围同时匹配 |
| 疑似受影响 | 依赖存在，但版本或生效路径尚未完全还原 | 传递依赖路径未完全还原 |
| 需要验证 | 漏洞信息、版本范围或项目依赖事实还未核实完整 | 证据链不完整 |
| 证据不足 | 无法建立可靠映射 | 无法获取关键证据 |

## 严重级别

| Severity | CVSS Score |
|----------|------------|
| Critical | 9.0 - 10.0 |
| High | 7.0 - 8.9 |
| Medium | 4.0 - 6.9 |
| Low | 0.1 - 3.9 |

## 修复优先级

1. 已确认的 `Critical` 和 `High` 级运行时漏洞
2. 涉及外部暴露面、反序列化、远程代码执行、身份绕过等高风险路径的问题
3. 被多个模块复用的公共传递依赖
4. 难以后续治理的第三方 JAR 内嵌组件问题
5. 利用条件较高的 `Medium` 和 `Low` 级问题

## 常见问题

### Q1: 扫描器报告漏洞，但 dependency:tree 显示的是安全版本？

可能原因：
- pom.xml 声明版本是有漏洞的，但被 `dependencyManagement` 覆盖到安全版本
- 传递依赖显式排除了有漏洞的组件

核对方法：检查 dependency:tree 输出的实际版本，而非 pom.xml 声明。

### Q2: 同一个依赖多个版本出现在依赖树中？

这是正常的。Maven/Gradle 使用"最近定义"原则。检查：
- 哪个版本最终进入 runtime classpath
- 是否有显式的版本强制（force）或覆盖

### Q3: 如何判断漏洞是否真实影响项目？

检查清单：
1. [ ] 依赖是否在 runtime classpath（而非 compileOnly/test）
2. [ ] 当前使用版本是否在受影响范围内
3. [ ] 漏洞触发条件是否在项目场景中满足
4. [ ] 是否有版本覆盖或 exclusion 规避了漏洞

### Q4: Gradle implementation 配置的依赖会传递吗？

不会。`implementation` 配置的依赖默认不传递。
如果需要传递，使用 `api` 配置。

### Q5: Spring Boot fat JAR 中的依赖如何分析？

1. 解压 JAR：`unzip -q app.jar -d tmp`
2. 查看 `BOOT-INF/lib/` 目录
3. 检查每个 JAR 的 POM 元数据
4. 使用 `jdeps --list-deps` 分析实际依赖

### Q6: 漏洞扫描工具的结果可以信任吗？

不能直接信任。扫描器只是线索，必须验证：
1. 实际生效版本（依赖树输出）
2. 受影响的精确版本范围
3. 漏洞是否已被修复
4. 项目是否真正会触发漏洞条件

## 参考链接

- [Maven Dependency Mechanism](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)
- [Gradle Viewing Dependencies](https://docs.gradle.org/current/userguide/viewing_debugging_dependencies.html)
- [CVE 官方数据库](https://www.cve.org/)
- [Spring Security Advisories](https://spring.io/security)
- [OSV API 文档](https://osv.dev/docs/)
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)