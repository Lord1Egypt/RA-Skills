---
name: openclaw-novel-write
<<<<<<< HEAD
version: 0.1.0
=======
version: 0.1.2
>>>>>>> 3a77ccf (chore: 版本更新至0.1.2)
description: OpenClaw 小说创作 Skill - 基于七步方法论的 AI 辅助写作系统
tags:
  - novel
  - writing
  - creative-writing
  - chinese
  - fiction
author: MartinYing
homepage: https://clawhub.ai
based-on: https://github.com/wordflowlab/novel-writer-skills
acknowledgments: |
  本 Skill 基于 wordflowlab/novel-writer-skills 改编，
  继承了其七步方法论和写作知识库。
---

# Novel Write Skill - OpenClaw 小说创作系统

## 概述

基于七步方法论的 OpenClaw Skill，用于在 OpenClaw 环境下完成 AI 辅助小说创作。支持都市、古代、玄幻、悬疑等多种题材，内置反AI检测写作规范。

**核心特点**：AI 自动分析用户描述，推荐风格和知识库，用户确认后继续。

## 核心能力

- 📚 **七步方法论**：从宪法到写作的完整创作流程
- 🔄 **六阶段写作**：预写分析 → 初稿生成 → 自检 → 文笔润色 → 修订 → 元数据输出
- 🤖 **AI 智能分析**：自动判断类型、推荐风格和知识库
- ✅ **用户确认机制**：每步分析结果需用户确认，可修改
- 🔍 **自动追踪**：角色状态、情节进度、线索管理、伏笔回收
- 🗺️ **情节图解**：Mermaid 关系图、战斗图、势力图自动生成
- 📝 **记忆系统**：.learnings/ 记录中途灵感，确保设定不丢失
- 📖 **失败记录**：fail-log 持续积累问题，持续优化
- ✍️ **反AI检测**：内置自然化写作规范，避免AI味
- 📊 **质量分析**：一致性、节奏、视角、对话检查、五视角读者反馈
- 🎯 **按卷分拆**：任务细化到章节，含字数要求

## 七步方法论

```
1. /novel init           → 初始化项目
2. /novel constitution   → 创建宪法 + AI分析风格偏好
3. /novel specify        → 定义规格 + AI分析类型（自动加载知识库）
4. /novel clarify       → 澄清关键决策
5. /novel plan          → 制定创作计划
6. /novel timeline      → 生成时间线 + 互相校验（新增）
7. /novel track-init    → 初始化追踪系统
8. /novel tasks         → 分解任务清单
                          ↓
开始写作 ↓
          ↓
9. /novel write [章节]  → 六阶段写作（预写→初稿→自检→润色→修订→元数据）
10. /novel track --check → 自动追踪验证
11. /novel analyze      → 每5章质量分析（含5视角读者反馈）
```

## 核心命令

### 触发方式

| 命令 | 触发关键词示例 |
|------|--------------|
| `/novel init [项目名]` | "创建新小说项目"、"初始化项目" |
| `/novel constitution` | "制定创作宪法"、"开始constitution" |
| `/novel specify` | "定义故事规格"、"开始specify" |
| `/novel clarify` | "澄清关键决策"、"clarify" |
| `/novel plan` | "制定创作计划"、"生成章节大纲" |
| `/novel track-init` | "初始化追踪系统" |
| `/novel tasks` | "分解任务清单"、"生成写作任务" |
| `/novel timeline` | "生成时间线"、"创建时间线文档" |
| `/novel write [章节]` | "写第X章"、"开始第一章"、"继续写"、"六阶段写作" |
| `/novel learnings` | "记忆系统"、"记录设定"、"更新记忆" |
| `/novel diagram` | "生成关系图"、"生成战斗图"、"势力图" |
| `/novel fail-log` | "失败记录"、"查看问题" |
| `/novel feedback` | "读者视角反馈"、"生成反馈报告" |

> **触发规则**：`/novel [命令]` 直接触发，或用中文描述意图（AI 自动识别）

### /novel init [项目名]
初始化新小说项目，创建标准目录结构。
- 自动创建追踪JSON文件
- 复制写作知识库

### /novel constitution
创建创作宪法，定义核心原则。
- AI 分析用户风格偏好，推荐预设风格
- 用户确认或修改后生成宪法

### /novel specify
定义故事规格（类型、角色、世界观、冲突等）
- AI 分析用户描述，自动判断小说类型
- 自动加载对应的 genres、styles、requirements
- 用户确认分析结果后生成规格文档

### /novel clarify
澄清关键决策（5个关键问题）

### /novel plan
制定创作计划（卷结构、章节、线索、伏笔、节奏）

### /novel track-init
从计划填充追踪系统（角色状态、关系网络、情节追踪）

### /novel tasks
生成按卷分拆的任务清单，含字数要求。**每卷单独md文件，tasks.md仅为总纲索引**。

### /novel write [章节编号]
执行章节写作。
- **必须先完成前8步**（init → constitution → specify → clarify → plan → timeline → track-init → tasks）
- **写完后强制检查**：字数验证 → 追踪验证 → 每5章质量分析，**任一失败阻断写作**
- 自动加载风格和规范
- 遵循反AI写作规范

### /novel track --check
追踪验证（字数、角色一致性、情节进度）

### /novel analyze
综合质量分析（**每5章提醒用户触发，失败阻断**）

## AI 自动分析机制

### constitution 步骤

AI 分析用户描述的风格偏好，推荐：
- 预设风格（自然人声/网文爽文/文学质感/古风典雅/极简白描）
- 写作规范（反AI-v4/快节奏/甜文/虐文/强情绪）

### specify 步骤

AI 分析用户描述的故事，自动判断：
- 题材类型（都市/古代/玄幻/悬疑等）
- 故事风格（甜宠/爽文/虐文等）
- 主角定位（普通人/豪门/重生/穿越等）
- 金手指类型（隐藏身份/特殊能力等）

并自动加载对应的知识库文件。

### 确认机制

每步分析后展示结果，用户可以：
- 直接确认（"OK"）
- 修改某项
- 补充更多信息

## 写作知识库

| 目录 | 内容 |
|------|------|
| `genres/` | 5种小说类型知识（romance, mystery, revenge, historical, wuxia） |
| `styles/` | 写作风格（5种预设） |
| `requirements/` | 写作规范（反AI-v4、快节奏、甜文、虐文等） |

## 自动化规则

- **after_each_chapter**：每次写作后自动 `/novel track --check`（**强制，失败阻断**）
- **every_5_chapters**：每5章提醒用户执行 `/novel analyze`（含5视角读者反馈，**强制，失败阻断**）

## 项目结构

```
<项目名>/
├── memory/
│   ├── constitution.md          # 创作宪法
│   └── style-reference.md       # 风格参考
├── stories/
│   └── <项目>/
│       ├── specification.md     # 故事规格
│       ├── clarify-answers.md  # 关键决策澄清
│       ├── creative-plan.md     # 创作计划
│       ├── timeline.md          # 时间线文档（新增）
│       ├── tasks.md             # 任务总纲（索引）
│       ├── tasks-volume-1.md    # 第1卷任务
│       ├── tasks-volume-2.md    # 第2卷任务
│       └── content/             # 正文
│           └── volumeX/
│               └── chapter-XX.md
├── spec/
│   ├── knowledge/               # 项目知识库
│   └── tracking/                # 追踪文件
│       ├── character-state.json
│       ├── relationships.json
│       ├── plot-tracker.json
│       ├── progress.json
│       └── validation-rules.json
└── .claude/
    └── knowledge-base/          # 写作知识库
        ├── genres/
        ├── styles/
        └── requirements/
```

## 反AI检测写作规范

核心要点：
- 30%-50% 段落应为单句成段
- 每段控制在 50-100 字
- 避免 AI 高频词（唯一的、直到、弥漫、摇摇欲坠等）
- 具象化描写（具体时间、人物、数量、场景）

详见 `commands/write.md`

## 使用示例

```
用户: 帮我创建一个新小说项目
      → 触发 /novel init

用户: 我想写一个都市甜宠文，男主是霸总
      → 触发 /novel constitution
      → AI 分析推荐：网文爽文 + romance-sweet
      → 用户确认 OK

用户: 继续描述故事
      → 触发 /novel specify
      → 描述：男主是霸道总裁，女主是普通上班族...
      → AI 分析：都市言情 × 豪门 + 甜宠
      → 自动加载：romance.md + web-novel.md + romance-sweet.md
      → 用户确认 OK

用户: 好的，继续下一步
      → 触发 /novel clarify

用户: 开始制定计划
      → 触发 /novel plan

用户: 开始分解任务
      → 触发 /novel track-init + /novel tasks

用户: 开始写第一章
      → 触发 /novel write
      → ⚠️ 前置检查（前6步）→ 全部通过 → 开始写作
      → 完成后自动 /novel track --check

用户: 继续写第5章
      → 触发 /novel write
      → ⚠️ 前置检查 → 通过 → 开始写作
      → 每5章提醒 → 用户触发 /novel analyze
```

## 依赖

- OpenClaw
- bash（用于辅助脚本）


