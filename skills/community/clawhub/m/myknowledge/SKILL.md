---
name: myknowledge
slug: my-knowledge
displayName: MyKnowledge
description: 创建知识库、管理项目文档、记录需求、整理个人知识。Create knowledge bases, manage project docs, track requirements, and organize personal knowledge.
version: "1.4.89"
author: CoderMoray
tags: 
  - "knowledge-base"
  - "knowledge-management"
  - "project-management"
  - "documentation"
  - "需求管理"
  - "知识库"
  - "项目管理"
  - "文档管理"
  - "笔记"
  - "个人知识"
category: "productivity"
---

# MyKnowledge Skill

## 概述

MyKnowledge 是一个通用的知识库管理 Skill，帮助用户：
- 创建标准化的知识库目录结构
- 管理需求生命周期（创建、更新、归档）
- 维护 PROJECT-STATUS.md 项目状态快照
- 导出/导入知识库（跨用户分享、备份迁移）
- 支持个人知识管理和项目文档管理

> **关于存储路径的说明**：本 Skill 默认将知识库存储在 `~/.myknowledge/` 目录下。这是**用户明确授权的知识库存储路径**，不是系统配置文件。本 Skill 只会访问用户明确授权的路径，不会访问其他系统配置文件。

## 首次使用引导

### 1. 检测初始化状态

加载本 Skill 时，首先检查 `skill-state.yaml`：
- **存在** → 跳过引导，正常使用
- **不存在** → 执行首次引导（约 1 分钟）

### 2. 首次引导流程

**步骤 1：欢迎与介绍**

```
AI：👋 欢迎使用 MyKnowledge！

我是你的智能知识库助手，可以帮你：
1. 自动整理项目资料
2. 记录要做的事情
3. 跟踪任务进度
4. 自动帮你做记录（可选）
```

**步骤 2：平台确认**

```
AI：你使用什么 AI 助手？
[CodeBuddy] [WorkBuddy] [OpenClaw] [其他] [帮我检测]
```

**步骤 3：自动记录设置**

```
AI：是否开启「自动记录」？

当你说的事情比较复杂时（如"分析数据"），
我会自动帮你创建记录。

1 — 开启（推荐）：自动帮你创建记录
2 — 关闭：你来手动控制

💡 随时可以说"开启/关闭自动记录"修改
```

**步骤 4：保存配置**

创建 `skill-state.yaml` 记录用户选择，包含：
- 平台类型
- 自动记录开关
- 引导完成标记

**重要**：引导只在首次使用时显示，之后不再出现。

**步骤 5：引导结束**

```
AI：🎉 设置完成！记住这几句话：
• "创建知识库" - 开始新项目
• "项目进展如何？" - 查看状态
• "继续之前的项目" - 恢复工作
• "导入知识库" - 导入别人分享的知识包
  （说"导入知识库"然后提供对应的知识文件给我即可）

✅ 引导已完成，下次不再显示
💡 如需重新查看，说"重新初始化"
```

## 使用模式

### 模式 1：主动使用

用户显式请求创建知识库（默认走全局，不询问类型）：

```
用户：创建知识库
AI：（自动创建到 ~/.myknowledge/global/{项目名}/）
     📁 已创建知识库「{项目名}」
     
用户：在当前目录创建知识库
AI：（在项目目录创建 .myknowledge/）
```

### 模式 2：自动检测

AI 检测到复杂任务时自动创建知识库并告知用户：

```
用户：帮我分析这个销售数据
AI：（检测到复杂任务）
    🔇 已自动创建知识库「销售数据分析」和需求 REQ-20260608-001
```

**复杂任务检测规则**：
- **关键词**（满足 3 个及以上触发）：分析、统计、挖掘、开发、设计、调研、整理、清洗、项目
- **任务特征**：多步骤操作、需要长期跟踪、涉及数据或文档

## 知识库结构

### 全局知识库

```
~/MyKnowledge/global/
├── README.md
├── requirements/
├── public/
├── archive/
└── PROJECT-STATUS.md
```

### 项目知识库

```
{project-path}/.myknowledge/
├── README.md
├── requirements/
├── public/
├── archive/
└── PROJECT-STATUS.md
```

## 核心功能

### 1. 创建知识库

```
输入：
- 类型（全局/项目）
- 名称（可选）

输出：
- 完整的知识库目录结构
- 初始化的 PROJECT-STATUS.md
```

### 2. 创建需求

```
输入：
- 需求标题
- 需求描述

输出：
- 需求目录 requirements/REQ-YYYYMMDD-XXX/
- 需求文档 README.md
- 更新的 PROJECT-STATUS.md
```

### 3. 更新需求状态

支持状态流转：
- Created → In Progress → Review → Done
- Created → Cancelled

### 4. 导出/导入知识库

```
用户：导出项目「销售分析」
AI：打包为 myknowledge-export-销售分析.zip
    → 包含项目状态 + 需求索引 + 安装引导

用户：导入知识库
AI：解压到全局知识库 → 同名项目提供覆盖/重命名/对比选项
```

### 5. 会话恢复

```
用户：继续 xxx 项目
AI：读取 PROJECT-STATUS.md...
    恢复项目状态，继续工作
```

## 平台适配

### OpenClaw（Hook 事件驱动）

通过 Hook 在消息到达时主动触发检测，不依赖 AI 是否注意到：
- `message:received` → 检测任务复杂度
- 更可靠地自动创建知识库和记录需求（操作后告知用户）
- 详细配置参考：`hooks/openclaw/hook-guide.md`

> **注意**：OpenClaw 的 Hook 模式是"后台运行（操作后告知）"，并非"无感知"。首次检测到大任务时会询问用户是否开启自动记录。

### CodeBuddy/WorkBuddy（意图识别）

通过 `description` 匹配和 Prompt 逻辑：
- AI 自动判断是否需要创建知识库
- 操作前会提示用户确认

### Claude（意图识别）

通过意图识别检测复杂任务，AI 自动判断是否创建知识库（操作前提示用户）。

> ⚠️ Hook 支持取决于具体 Claude 环境，默认通过意图识别工作。如有 Hook 需求，参考 `hooks/claude/README.md`。

## 文件说明

| 文件/目录 | 用途 |
|-----------|------|
| `SKILL.md` | 本文件，Skill 主入口 |
| `settings.yaml` | Skill 配置 |
| `core/` | 核心功能（主逻辑、模板） |
| `modules/` | 可选模块（懒加载：管理、更新、错误处理、智能任务追踪） |
| `one-time/` | 一次性配置（首次引导、安装源检测） |
| `hooks/` | 平台 Hook（OpenClaw、Claude） |
| `test/` | 测试套件（开发用，AI 忽略） |

> **AI 助手注意**：`test/` 目录仅供开发和测试使用，正常响应用户请求时请忽略。

## 用户支持

> **AI 助手注意**：遇到以下情况时，引导用户查看对应文档（都在 Skill 目录下）。

| 用户遇到... | 引导查看 |
|------------|---------|
| 常见使用问题 | `FAQ.md` — 按主题分类的问答（智能任务追踪、平台差异、备份等） |
| 踩坑了 | `docs/PITFALLS.md` — 19 个真实使用坑及正确做法 |
| 不知道怎么用 | `README.md` — 快速开始 + 使用场景 + 高手技巧 |
| 需要重新初始化 | 说"重新初始化 MyKnowledge"即可重置 |

## 依赖

- 文件系统操作能力
- 模板渲染能力
- （可选）OpenClaw Hook 支持

## 许可证

Apache License 2.0
