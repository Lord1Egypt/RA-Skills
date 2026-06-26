# openclaw-memory-transfer

> **OpenClaw 零摩擦记忆迁移。** 从 ChatGPT、Claude、Gemini、Copilot 等平台带走你的记忆——10 分钟搞定。

[![Powered by MyClaw.ai](https://img.shields.io/badge/Powered%20by-MyClaw.ai-blue)](https://myclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[English](README.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [Italiano](README.it.md) | [Español](README.es.md)

---

你在 ChatGPT 上聊了几个月甚至几年，它知道你的写作风格、项目进度、各种偏好和习惯。切换到 OpenClaw 的时候，这些不应该从零开始。

**Memory Transfer** 把旧 AI 知道的关于你的一切提取出来，清洗整理后导入 OpenClaw 的记忆系统。只需要告诉你的 Agent 你从哪来。

## 怎么用

对你的 OpenClaw Agent 说：

```
我之前用的是 ChatGPT，想把记忆带过来
```

或者：

```
从 Gemini 迁移我的数据
```

Agent 会一步步引导你完成，全程白话，不需要学任何东西。

## 支持的平台

| 来源 | 方式 | 你需要做什么 |
|------|------|-------------|
| **ChatGPT** | ZIP 数据导出 | 在设置里点导出，上传 ZIP |
| **ChatGPT**（备选） | Prompt 引导 | 复制一段话过去，结果贴回来 |
| **Claude.ai** | Prompt 引导 | 复制一段话过去，结果贴回来 |
| **Gemini** | Prompt 引导 | 复制一段话过去，结果贴回来 |
| **Copilot** | Prompt 引导 | 复制一段话过去，结果贴回来 |
| **Perplexity** | Prompt 引导 | 复制一段话过去，结果贴回来 |
| **Claude Code** | 自动扫描 | 什么都不用做 |
| **Cursor** | 自动扫描 | 什么都不用做 |
| **Windsurf** | 自动扫描 | 什么都不用做 |

### ChatGPT ZIP 导出（推荐）

最完整的迁移方式。ChatGPT 的数据导出包含完整对话历史，解析器自动提取：

- 📝 你的写作风格特征
- 🔧 你常用的工具和平台
- 📊 你最常让 AI 做什么（写代码、分析、写文案等）
- 🚫 你纠正过 AI 的模式（"别这样做"）
- 💬 你常讨论的话题

### Prompt 引导导出

对于没有结构化导出的云端 AI，你的 Agent 给你**一段 prompt**，发给旧 AI，它会输出所有关于你的信息。复制回来就行。

### 本地 Agent 自动扫描

如果你用过 Claude Code、Cursor 或 Windsurf，skill 自动扫描本地配置文件——零操作。

## 迁移什么

| 类别 | 写入位置 | 示例 |
|------|---------|------|
| 身份信息 | `USER.md` | 姓名、职业、语言、时区 |
| 沟通风格 | `USER.md` | 写作语气、格式偏好 |
| 知识经验 | `MEMORY.md` | 项目、领域专长、洞察 |
| 行为模式 | `MEMORY.md` | 工作流、习惯、纠正记录 |
| 工具偏好 | `TOOLS.md` | 技术栈、平台、环境配置 |

## 绝对不迁移的

- 🔒 API Key、Token、密码
- 🔒 认证凭证
- 🔒 敏感个人数据（除非你明确要求）

所有导入的数据会先展示给你确认，不会静默写入任何内容。

## 安装

### OpenClaw（通过 ClawHub）

```bash
clawhub install openclaw-memory-transfer
```

### 手动安装

```bash
cp -r . ~/.openclaw/skills/openclaw-memory-transfer/
```

## 迁移体验

```
你：我之前用的 ChatGPT，想把东西搬过来

Agent：最简单的方式——去 ChatGPT 导出你的数据：
       1. Settings → Data Controls → Export Data
       2. 点 Export，你会收到一封邮件
       3. 下载 ZIP 发给我，我自动解析

你：[上传 ZIP]

Agent：解析完成！找到 847 条对话。整理如下：

       📋 迁移预览
       写入 USER.md：Leo, 创业者, 中英文双语...
       写入 MEMORY.md：MyClaw 项目, 增长策略...
       写入 TOOLS.md：Node.js, React, Netlify...

       有什么要改的吗？

你：没问题，写入吧

Agent：✅ 迁移完成！现在我知道你是谁了。
```

## 项目结构

```
openclaw-memory-transfer/
├── SKILL.md                           # Agent skill 定义
├── scripts/
│   └── parse-chatgpt-export.js        # ChatGPT ZIP 解析器（Node.js，零依赖）
├── README.md                          # 英文文档
├── README.zh-CN.md                    # 本文件
└── LICENSE                            # MIT
```

## 贡献

欢迎提 Issue 和 PR。如果你想新增一个 AI 平台的支持：

1. 在 `SKILL.md` 中添加导出方式（prompt 模板或文件扫描路径）
2. 如果有结构化导出，在 `scripts/` 中添加解析器
3. 更新支持平台表格

## 许可证

MIT — 随便用。

---

**Powered by [MyClaw.ai](https://myclaw.ai)** — 给每个用户一台完整服务器的 AI 个人助手平台。
