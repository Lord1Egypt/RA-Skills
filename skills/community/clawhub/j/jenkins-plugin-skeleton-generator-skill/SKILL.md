---
description: 根据用户提供的Jenkins版本和JDK版本生成Jenkins插件骨架。
name: jenkins-plugin-skeleton-generator-skill
activation:
  - 用户请求创建/生成/搭建/开发 Jenkins 插件
  - User requests to create/generate/build/develop a Jenkins plugin
---

# Jenkins插件骨架生成器技能

## 目的

生成与用户环境匹配的Jenkins插件基础结构。

**重要规则**：本技能**不得**假定默认的Jenkins版本或JDK版本。在用户确认版本之前，**请勿生成任何文件**。

### 语言规则

**交互语言**（对话、提问、校验提示）：自动检测用户消息语言并保持一致。

**输出语言**（代码注释、README.md）：在收集信息时**主动询问**用户偏好。用户未指定则以交互语言为默认。

| 选项 | 生成结果 |
|------|---------|
| 中文 | `README.md`（中文）+ 中文代码注释 |
| English | `README.md`（英文）+ 英文代码注释 |
| 中英双语 | `README.md`（交互语言）+ `README.en.md`（英文） + 代码注释用交互语言 |
| 日本語等 | 对应语言的 README + 注释 |

询问模板：
```
中文交互 → "生成的代码注释和 README 用什么语言？（默认中文，也可选 English、中英双语、日本語等）"
English  → "What language for generated code comments and README? (Default: English, or zh-CN, bilingual, ja, etc.)"
```


---

## 目录结构

```
SKILL.md                          # 本文件：工作流指令
templates/                         # 代码与配置模板
  ├── pom.md                        # Maven POM 模板
  ├── repository-config.md         # Maven 仓库配置片段
  ├── builder.md                   # Builder 扩展点模板
  ├── run-listener.md              # RunListener 扩展点模板
  ├── async-periodic-work.md       # 异步任务模板
  ├── plugin-configuration.md      # 持久化配置模板
  ├── config-jelly.md              # Jelly 配置界面模板
  ├── readme-template.md           # 项目 README 模板
  └── project-structure.md         # 项目目录结构
references/                        # 参考文档
  ├── plugin-types.md             # 插件类型 / 扩展点对照表
  ├── trigger-timing-reference.md # 触发时机参考表
  ├── compatibility-check.md      # 兼容性检查清单
  ├── troubleshooting.md          # 故障排查指南
  └── jelly-reference.md          # Jelly 控件完整参考
```

---

## 执行前所需的输入信息

请向用户询问以下信息：

1. **Jenkins版本**（例如：2.401.1）
2. **JDK版本**（例如：11、17、21）
3. **Maven版本**（可选）
4. **插件元数据**：
   - 插件名称（Display Name）
   - groupId
   - artifactId
   - 包名（package name）

5. **插件类型 / 扩展点**（明确选择）：
   - [ ] Builder（构建步骤）
   - [ ] Publisher（构建后发布者）
   - [ ] Trigger / SCM（触发器）
   - [ ] Action（界面操作）
   - [ ] Listener（系统事件监听器）
   - [ ] QueueTaskDispatcher（队列任务分发）
   - [ ] ComputerListener（节点监听器）
   - [ ] 其他：_______

6. **触发时机**（与扩展点对应）：
   - 构建执行阶段触发
   - 构建完成后触发
   - 定时/轮询触发
   - 界面交互触发
   - 系统事件触发
   - 节点状态变更触发

7. **是否需要异步执行**：□ 是 □ 否
8. **是否需要持久化配置**：□ 是 □ 否
9. **是否需要全局配置页面**：□ 是 □ 否
10. **输出语言**（生成的代码注释和 README 的语言）：默认与交互语言一致，也可指定为 English、日本語等

---

## 工作流程

### 第一步：环境信息收集与分析

收集用户提供的所有信息后，进行兼容性分析：

- Jenkins API兼容性检查
- Java语言级别确认
- Jenkins Plugin Parent版本选择
- 依赖版本确定

**输入验证与纠错**（在生成文件前必须执行）：

以下为校验规则，**每条包含中/英双语提示**，根据交互语言选对应版本输出。

---

**① 必填项检查**

Jenkins 版本和 JDK 版本缺一不可 → **追问**：

> ⚠️ 还需要一个信息：请问你使用的 **Jenkins 版本**（如 2.401.1）和 **JDK 版本**（如 17）是什么？
>
> ⚠️ One more thing: what **Jenkins version** (e.g. `2.401.1`) and **JDK version** (e.g. `17`) are you using?

---

**② 版本格式校验**

| 字段 | 合法格式 | 非法示例 |
|------|---------|---------|
| Jenkins 版本 | `x.y.z`（如 `2.401.1`） | `2.401`、`latest`、`LTS` |
| JDK 版本 | 纯数字（`8`、`11`、`17`、`21`） | `jdk17`、`1.8`、`17.0` |

检测到非法格式 → **指出并给示例**：

> ⚠️ `[值]` 不是合法的 `[Jenkins/JDK]` 版本格式。Jenkins 版本请用 `x.y.z`（如 `2.401.1`），JDK 请用数字（如 `17`）。请重新提供。
>
> ⚠️ `[value]` is not a valid `[Jenkins/JDK]` version. Use `x.y.z` (e.g. `2.401.1`) for Jenkins, a number (e.g. `17`) for JDK. Please re-enter.

---

**③ Jenkins 与 JDK 兼容性校验**

| Jenkins | 最低 JDK | 说明 |
|---------|---------|------|
| < 2.361 | JDK 8 | EOL |
| 2.361-2.419 | JDK 11 | |
| 2.420-2.462 | JDK 17 | |
| 2.463+ | JDK 17/21 | |

不兼容 → **给出问题 + 两个选择**：

> ⚠️ Jenkins `[A]` 要求 JDK `[B]`+，你提供的是 JDK `[C]`。请 ① 升级 JDK 到 `[B]` 或 ② 降低 Jenkins 版本。
>
> ⚠️ Jenkins `[A]` requires JDK `[B]`+, but you specified JDK `[C]`. Options: ① upgrade JDK to `[B]`+ or ② downgrade Jenkins.

---

**④ Parent POM 确定**

| Jenkins | Parent POM |
|---------|-----------|
| 2.361.x | 4.66 |
| 2.401.x | 4.75 |
| 2.426.x | 4.80 |
| 2.440.x | 4.83 |
| 2.462.x | 4.85 |

不匹配时告知：

> ℹ️ 未精确匹配，已选 Parent POM `4.XX`（≤ Jenkins 版本的最新版）。
>
> ℹ️ No exact match, auto-selected Parent POM `4.XX` (latest ≤ Jenkins version).

---

**汇总**（校验通过后）：

> ✓ 校验通过 | Jenkins `[版本]` + JDK `[版本]` + Parent POM `4.XX` + 输出语言 `[语言]`
>
> ✓ Passed | Jenkins `[ver]` + JDK `[ver]` + Parent POM `4.XX` + Output `[lang]`

> 详细兼容性检查项目见 `references/compatibility-check.md`
> 构建或运行中遇到问题见 `references/troubleshooting.md`

### 第二步：触发时机与扩展点设计

根据用户选择的插件类型，参考扩展点对照表确定代码模板。

> 完整扩展点与触发时机对照见 `references/plugin-types.md` 和 `references/trigger-timing-reference.md`

### 第三步：生成项目结构

按照 Maven HPI 项目标准生成目录结构。

> 标准目录结构见 `templates/project-structure.md`

### 第四步：README 生成

根据用户选择的输出语言，用 `templates/readme-template.md` 生成对应语言的 `README.md`。章节标题和说明文字必须用输出语言。

| 占位符 | 来源 | 填充示例 |
|--------|------|---------|
| `{{PLUGIN_DISPLAY_NAME}}` | 用户提供的插件名称 | `构建审计插件` |
| `{{PLUGIN_DESCRIPTION}}` | 根据插件类型自动生成一段简要描述 | `记录每次构建的关键信息到日志，支持自定义日志级别和输出格式` |
| `{{JENKINS_VERSION}}` | 用户提供的 Jenkins 版本 | `2.426` |
| `{{JDK_VERSION}}` | 用户提供的 JDK 版本 | `17` |
| `{{MAVEN_VERSION}}` | 用户提供的 Maven 版本（未提供则填"3.6+"） | `3.6+` |
| `{{EXTENSION_TYPE}}` | 用户选择的插件类型 | `RunListener` |
| `{{TRIGGER_TIMING}}` | 用户选择的触发时机 | `构建开始和完成时自动触发` |
| `{{FEATURE_LIST}}` | 根据异步/持久化/全局配置开关动态拼接（无则留空） | `- 异步执行：每 5 分钟清理一次过期日志` |
| `{{ARTIFACT_ID}}` | 用户提供的 artifactId | `build-auditor` |
| `{{PACKAGE_PATH}}` | 包名对应的路径（如 `com/example/plugin`） | `com/company/audit` |
| `{{MAIN_CLASS}}` | 主扩展类名 | `BuildAuditorListener` |
| `{{USAGE_TITLE}}` | 根据插件类型生成标题：Builder→"在项目中使用"，Publisher→"配置构建后操作"，RunListener→"自动监听"，Trigger→"设置定时触发" | `自动监听` |
| `{{USAGE_DESCRIPTION}}` | 根据插件类型生成编号步骤，以"打开 Jenkins 项目配置"开头 | `1. 项目启动后自动生效\n2. 无需额外配置` |
| `{{CONFIGURATION_DETAILS}}` | 无持久化配置则省略；有则说明配置保存位置 | `所有配置项均保存在 Jenkins 全局配置中，重启不会丢失。` |
| `{{CONFIG_ITEMS}}` | 如无配置项则填 `| - | - | - | (无配置项) |`；有则根据 Java 类字段名和类型生成表格行 | `\| message \| 字符串 \| Hello Jenkins \| 构建时输出的消息 \|` |
| `{{LICENSE_INFO}}` | 默认 MIT License | `MIT License` |

### 第五步：Maven配置生成

根据用户输入生成 `pom.xml`。**必须注意**：

- 生成的 `pom.xml` 默认必须同时配置 `<repositories>` 与 `<pluginRepositories>`，不应假设用户已配置 Maven `settings.xml`
- **除非用户明确指定其他仓库**，否则始终默认使用 Jenkins 官方 Repository Proxy（`https://repo.jenkins-ci.org/public/`），不应默认依赖 Maven Central、阿里云镜像或企业 Nexus

生成时参考以下模板：

- 仓库配置片段：`templates/repository-config.md`
- 完整 POM 模板：`templates/pom.md`

应避免：不支持的 API、依赖冲突、servlet 命名空间问题。

### 第六步：插件代码生成

根据插件类型生成代码。**代码注释必须用输出语言**（如用户选 English 则 `// Build logic`，选中文则 `// 构建逻辑`）。

| 插件类型 | 模板 |
|---------|------|
| Builder | `templates/builder.md` |
| RunListener | `templates/run-listener.md` |
| AsyncPeriodicWork | `templates/async-periodic-work.md` |
| 持久化配置 | `templates/plugin-configuration.md` |

### 第七步：资源文件生成

根据是否需要配置界面，生成对应的Jelly文件。

生成 `config.jelly` 时，根据 Java 类中的字段类型选择对应控件：

- `templates/config-jelly.md` — 基础模板 + 字段类型→控件映射表
- `references/jelly-reference.md` — 全部可用控件（textbox、checkbox、password、textarea、number、dropdownList、select、radioBlock、repeatable）及用法示例

> 生成后必须核对 Jelly 中 `field` 属性与 Java getter/setter 的对应关系（见 jelly-reference.md 末尾的命名对照表）。

### 第八步：构建与测试

提供构建命令：

```bash
# 清理并打包
mvn clean package

# 本地测试运行
mvn hpi:run

# 仅打包不测试
mvn clean package -DskipTests

# 生成IDE项目文件
mvn eclipse:eclipse   # Eclipse
mvn idea:idea         # IntelliJ IDEA
```

输出位置：`target/插件名称.hpi`

### 第九步：安装与验证

安装步骤：

1. 登录Jenkins
2. 进入 **Manage Jenkins** → **Plugins** → **Available** → **Advanced**
3. 在 **Upload Plugin** 区域，选择生成的 `.hpi` 文件
4. 点击 **Upload** 上传
5. 重启Jenkins（如需要）
6. 验证插件在 **Installed** 列表中显示
7. 根据插件类型，在相应位置测试功能

验证清单：

- [ ] 插件成功上传并安装
- [ ] Jenkins日志无报错
- [ ] 配置界面正常显示
- [ ] 触发逻辑按预期执行
- [ ] 构建日志输出正确信息
- [ ] 异步任务正常运行（如适用）

---

## 输出要求

生成完整的插件项目后，提供以下内容：

1. **技术设计说明** - 插件架构、扩展点选择、触发时机说明
2. **README.md** - 完整的项目 README（功能、安装、使用、开发）
3. **目录结构** - 完整的项目文件树
4. **pom.xml** - 完整的Maven配置文件
5. **Java源代码** - 所有扩展类和配置类
6. **资源文件** - Jelly配置界面、帮助文档、国际化文件
7. **测试代码** - 单元测试和集成测试（可选）
8. **构建步骤** - 详细的构建命令
9. **安装步骤** - 插件安装和验证指南
10. **触发时机说明** - 明确说明各扩展点的触发时机
11. **故障排除** - 常见问题和解决方法

---

## 常见问题与排查

当用户反馈构建失败、安装异常或运行时错误时，请参考以下排查路径：

### 快速诊断流程

1. **先确认输入**：检查 Jenkins 版本与 JDK 版本是否兼容（见第一步的兼容性校验表）
2. **再确认构建**：`mvn clean package -DskipTests` 是否通过
3. **最后确认运行**：`mvn hpi:run` 是否正常启动

### 典型问题速查

| 症状 | 可能原因 | 排查方向 |
|------|---------|---------|
| 构建报依赖解析错误 | 仓库配置或 Parent POM 版本问题 | 检查 `pom.xml` 仓库地址和 Parent 版本 |
| UnsupportedClassFileVersionError | JDK 版本不匹配 | 核对 `java.level` 与本地 JDK |
| 端口被占用 | 8080 已被占用 | 改用 `-Djetty.port=9090` |
| .hpi 上传后报找不到依赖 | jenkins.version 过高 | 降低到 ≤ 运行中 Jenkins 版本 |
| 配置界面不显示 | config.jelly 字段不匹配 | 检查 field 与 getter/setter 一致性 |
| 异步任务未执行 | 缺少 @Extension 或周期设置 | 确认注解和 getRecurrencePeriod() |

> 详细排查步骤和解决方案见 `references/troubleshooting.md`

---

## 质量规则

生成的插件必须满足：

- [ ] 与用户要求的Jenkins版本匹配
- [ ] 与用户要求的JDK版本匹配
- [ ] 使用正确的扩展点类型
- [ ] 在正确的触发时机执行
- [ ] 能够成功构建（`mvn clean package`）
- [ ] 生成有效的HPI包
- [ ] README.md 包含完整的安装和使用说明
- [ ] 遵循Jenkins插件开发规范
- [ ] 包含完整的配置界面（如需要）
- [ ] 代码注释完整
- [ ] 无已知API冲突
- [ ] 无servlet命名空间问题

## 质量保证

- 与指定的 Jenkins 版本严格兼容
- 与指定的 JDK 版本严格兼容
- 构建零错误
- 遵循 Jenkins 插件开发最佳实践
- 最小化外部依赖

## 参考

- Jenkins 插件开发文档：https://www.jenkins.io/doc/developer/
- Plugin POM：https://github.com/jenkinsci/plugin-pom
- 示例插件：https://github.com/jenkinsci/hello-world-plugin/
