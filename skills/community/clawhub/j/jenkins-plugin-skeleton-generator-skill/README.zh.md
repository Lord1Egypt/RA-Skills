# Jenkins 插件骨架生成器

> 一句话描述需求，AI 自动生成完整的 Jenkins 插件项目骨架。

[![SKILLHUB](https://img.shields.io/badge/SKILLHUB-已发布-3b82f6)](https://www.skillhub.cn/skills/jenkins-plugin-skeleton-generator-skill)
[![ClawHub](https://img.shields.io/badge/ClawHub-已发布-f97316)](https://clawhub.ai/leoyim/skills/jenkins-plugin-skeleton-generator-skill)

[English](README.md)

## 安装

在 [SKILLHUB](https://www.skillhub.cn/skills/jenkins-plugin-skeleton-generator-skill) 或 [ClawHub](https://clawhub.ai/leoyim/skills/jenkins-plugin-skeleton-generator-skill) 中搜索「Jenkins 插件骨架生成器」并安装，或在终端执行：

```bash
skillhub install jenkins-plugin-skeleton-generator-skill
```

## 快速开始

在 OpenCode/Codex/Claude Code 等工具中对 AI 说类似以下的话即可触发该技能：

- 「帮我创建一个 Jenkins 插件」
- 「我要开发一个 Jenkins 插件，Jenkins 版本 2.401.1」
- 「生成一个 Jenkins Builder 插件骨架」

AI 会主动询问你当前环境中缺失的关键信息，无需一次性准备好所有参数。

## 需要准备什么

触发技能后，AI 会依次询问以下信息：

| 信息 | 说明 | 示例 |
|------|------|------|
| Jenkins 版本 | 目标 Jenkins 最低版本 | `2.401.1` |
| JDK 版本 | 项目使用的 Java 版本 | `11`、`17`、`21` |
| Maven 版本 | (可选) 本地 Maven 版本 | `3.9` |
| groupId | Maven 坐标 | `com.example.jenkins` |
| artifactId | 项目标识 | `hello-plugin` |
| 包名 | Java 包路径 | `com.example.jenkins.hello` |
| 插件类型 | 选择一种扩展点 | 见下方说明 |
| 输出语言 | 生成代码注释和 README 的语言 | `zh-CN`、`en`、`ja` 等 |
| 是否需要异步/持久化/全局配置 | 额外功能开关 | 是 / 否 |

## 支持哪些插件类型

- **Builder** — 自定义构建步骤（最常用）
- **Publisher** — 构建后处理（通知、归档等）
- **Trigger** — Cron 定时或 SCM 变更触发
- **Action** — 添加界面操作按钮
- **RunListener** — 监听构建生命周期事件
- **ComputerListener** — 监听节点上下线
- **QueueTaskDispatcher** — 任务分配调度

## 使用示例

### 示例一：最简单的 Builder 插件

**你说**：

> 帮我创建一个 Jenkins 插件，Jenkins 2.401，JDK 17，artifactId 是 my-build-step，做一个 Builder 类型的构建步骤插件

**AI 会生成**：

```
my-build-step/
├── pom.xml              # 含 Jenkins 官方仓库配置
├── README.md            # 完整的使用说明
├── .gitignore
└── src/
    └── main/
        ├── java/.../
        │   └── MyBuildStepBuilder.java   # Builder 扩展代码
        └── resources/.../
            └── MyBuildStepBuilder/
                ├── config.jelly            # 配置界面
                └── help.html
```

### 示例二：带持久化配置的 Listener

**你说**：

> 开发一个 Jenkins RunListener 插件，Jenkins 2.426，JDK 21，artifactId 叫 build-auditor，需要持久化配置，包名 com.company.audit

**AI 会生成**：

```
build-auditor/
├── pom.xml
├── README.md
├── .gitignore
└── src/
    └── main/
        ├── java/com/company/audit/
        │   ├── BuildAuditorListener.java    # RunListener
        │   └── config/
        │       └── PluginConfiguration.java  # 持久化配置类
        └── resources/
```

## Jenkins 开发新手？

如果你不熟悉 Jenkins 插件开发，以下是需要了解的几个核心概念（10 秒速览）：

| 概念 | 一句话解释 | 你通常需要的 |
|------|-----------|-------------|
| **扩展点 (Extension Point)** | Jenkins 预留的"钩子"，插件实现它来插入逻辑 | 选一个类型（Builder 最常用） |
| **Descriptor** | 描述"这个插件叫什么、怎么显示"，每个扩展点类都带一个 | 技能自动生成，不用管 |
| **config.jelly** | 用 XML 写的插件配置页面 | 技能根据你的字段类型自动选控件 |
| **hpi** | Jenkins 插件打包格式，类似 WAR 之于 Web 应用 | `mvn clean package` 后自动生成 |
| **DataBoundConstructor** | 标记"这些参数从配置页保存下来"的构造方法 | 技能自动加，不用手写 |

**第一次使用建议**：直接说「帮我创建一个 Jenkins Builder 插件，Jenkins 2.401.1，JDK 17」，技能会帮你完成剩下的。

## 生成后做什么

AI 会同时提供后续操作指引：

1. 进入项目目录执行 `mvn clean package` 构建
2. `mvn hpi:run` 本地启动 Jenkins 测试
3. 将生成的 `.hpi` 上传到 Jenkins 插件管理中心
4. 重启 Jenkins 后验证功能

## 已知限制

当前技能主要靠对话引导，在以下场景需要你多留意：

| 场景 | 影响 | 建议 |
|------|------|------|
| 输错版本号（如 `Jenkins 3.0`） | 可能生成错误的 Parent POM 版本 | 参考 [Jenkins 与 JDK 兼容表](https://www.jenkins.io/doc/book/platform-information/support-policy-java/index.html) 核对 |
| 版本组合不兼容（如 Jenkins 2.426 + JDK 11） | 构建或运行时报错 | 确保 JDK 版本 ≥ Jenkins 要求的最低版本 |
| 漏填必填信息 | 生成的项目不完整 | 仔细过一遍「需要准备什么」清单 |
| 自定义扩展点（非 7 种标准类型） | 不会自动生成该类型代码 | 选择最接近的类型后在生成结果上手动改造 |
| 复杂插件（多扩展点、自定义 Descriptor） | 一次只能生成一个主扩展点骨架 | 分多次生成再手动合并 |

遇到问题可查看项目内的 `references/troubleshooting.md`，或直接在对话中描述你遇到的现象。

## 提醒

- 技能不会假定默认版本——请明确告知 Jenkins 和 JDK 版本
- 默认使用 Jenkins 官方 Maven 仓库，无需额外配置 `settings.xml`
- 所有生成的代码都包含注释，可直接在此基础上进行二次开发
- **多语言支持**：生成的注释和 README 可以为中文、英文、日文等任意语言——告知 AI 即可
