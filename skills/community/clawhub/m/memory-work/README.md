<div align="center">

# Memory Work v2

**一套 AI 时代的注意力保护架构**

中文 | [English](#memory-work-v2-english)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude](https://img.shields.io/badge/Built%20for-Claude-blueviolet)](https://claude.ai)
[![Obsidian](https://img.shields.io/badge/Works%20with-Obsidian-purple)](https://obsidian.md)

</div>

> 你的 AI 不需要更聪明，它需要记住。

---

## 痛点

当你同时面对 10 个以上并行项目，传统 AI 助手反而让事情更糟：

- **AI 失忆**：每次对话从零开始，你要反复喂上下文
- **你成了瓶颈**：想法 → *自己*结构化 → *自己*录入 → *自己*维护
- **知识库成负担**：库越大，管理成本越高

## 解法

**Memory Work** 把流程反过来：

- 想法 → **直接口述** → AI 结构化 → AI 维护
- AI 启动时自动读取分层文件 → **不再失忆**
- 分区代理 → **可扩展到任意规模**

**你只负责两件事：提供注意力焦点，做创意决策。**

AI 负责其余：整合历史信息、匹配相关语料、执行结构化输出。

---

## 在 Claude Code 中如何使用

### 首次运行：智能初始化

克隆仓库后用 Claude Code 打开，AI 会自动：

```
1. 检测到这是全新安装
2. 询问你的偏好语言（中文 / English）
3. 收集你的基本信息，创建用户档案
4. 创建你的第一周工作区
5. 问你：「这周想做什么？」
```

**你不需要手动配置任何东西。** 直接开聊。

<div align="center">

![首次运行演示 - 语言选择](docs/images/first-run-demo.png)
*步骤 1：语言选择与文件初始化*

![首次运行演示 - 用户配置](docs/images/user-setup-demo-v2.png)
*步骤 2：口述式用户画像配置*

</div>

### 日常使用：口述优先

```
你："这周要把产品文档整理一下，周三有个客户会议要准备演示方案，
    另外那个合作协议让团队跟进一下。"

Claude：
1. 拆解为 3 个任务，写入 _本周.md
2. 搜索全库相关材料，摘录到参考材料区
3. 向你确认不确定的点
4. 主动询问：「要我生成日历文件吗？」
```

你自然口述，Claude 结构化。**心流状态受保护。**

### 周节奏

```
周一             →         周中            →          周五
  │                         │                         │
  ▼                         ▼                         ▼
┌─────────┐           ┌─────────┐            ┌─────────┐
│  口述   │           │  推进   │            │  归档   │
│   ↓     │           │   ↓     │            │   ↓     │
│AI 转化  │ ────────▶ │AI 补充  │ ─────────▶ │AI 校准  │
│   ↓     │           │   ↓     │            │   ↓     │
│  排程   │           │  产出   │            │  新周   │
└─────────┘           └─────────┘            └─────────┘
```

| 阶段 | 你做什么 | Claude 做什么 |
|------|----------|---------------|
| **周一** | 口述本周想做的事 | 拆解任务，拉取材料，生成日历 |
| **周中** | 工作，随时补充想法 | 跟踪进展，搜索全库，辅助决策 |
| **周五** | 对记忆操作给反馈 | 校准记忆，归档，创建下周 |

---

## 四层记忆架构

解决「AI 失忆」的核心机制。灵感来自 [Titans](https://arxiv.org/abs/2501.00663)（惊奇度驱动）和 [MemSkill](https://arxiv.org/abs/2501.03313)（可进化记忆）。

| 层级 | 文件 | 生命周期 | 用途 |
|------|------|---------|------|
| **持久层** | SOUL.md, USER.md | 极少变化 | 身份、价值观、方法论 |
| **工作层** | _本周.md | 周期刷新 | 当前任务和专注点 |
| **动态层** | MEMORY.md（特定区块） | 跨周保留，有衰减 | 洞见、决策、偏好 |
| **程序层** | MEMORY.md（特定区块） | 积累到稳定后毕业 | 行为模式、条件反射 |

### 记忆如何进化

```
对话 → AI 检测到「惊奇」→ 提议记住
              ↓
      你确认 → 写入记忆（带元数据）
              ↓
      周复盘 → 校准有用性 → 增强或衰减
```

**惊奇度驱动**：只有偏离已知模式的信息才会写入。没有噪音。

**用户确认**：AI 提议，你批准。未经同意不写入任何内容。

**有生命周期**：强记忆持久（★★★），弱记忆衰减（★☆☆ → 4 周未激活则归档）。

**记忆毕业**：稳定的模式从 MEMORY.md 自动升级到 USER.md，成为你的定义特征。

---

## 专注区：你的注意力锚点

`00 专注区/`（或 `00 Focus Zone/`）是整个系统的心脏：

```
00 专注区/
├── _本周.md           ← 当前的注意力焦点
├── MEMORY_LOG.md      ← 记忆系统自己的日志
├── ITERATION_LOG.md   ← 架构进化日志
└── _归档/             ← 历史周记录
```

<div align="center">

![Obsidian 中的专注区](docs/images/obsidian-focus-zone-demo.png)
*在 Obsidian 中查看专注区的完整结构*

</div>

**一周一个文件。** 周五归档，周一新建。你不需要管理积压——全部归档可检索。

---

## 架构一览（v2）

```
memory-work/
├── CLAUDE.md              # 系统入口（Cowork 自动注入）
├── SOUL.md                # AI 人格定义 & 协作风格
├── USER.md                # 你的档案 & 稳定偏好
├── MEMORY.md              # 长期记忆（动态层 + 程序层）
│
├── 00 Focus Zone/         # 英文版周工作台
├── 01 Materials/          # 个人档案库
├── 02 Tools/              # 提示词模板
├── 06 Skills/             # 自定义技能
│
├── docs/                  # 文档 & 截图
├── templates/             # 启动模板
│
└── zh-CN/                 # 完整中文版
    ├── CLAUDE.md
    ├── SOUL.md, USER.md, MEMORY.md
    ├── 00 专注区/
    ├── 01 你的项目/
    ├── 02 你的阅读/
    └── 03 你的写作/
```

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/yiliqi78/memory-work.git
```

或直接下载：[下载 ZIP](https://github.com/yiliqi78/memory-work/archive/refs/heads/main.zip)

### 2. 选择语言

- **中文**：使用 `zh-CN/` 目录
- **English**：直接使用根目录

### 3. 用 Claude Code / Cowork 打开

```bash
cd memory-work    # 或: cd memory-work/zh-CN
claude .
```

### 4. 开始对话

发送任意消息（如「启动」「开始工作」），Claude 自动检测首次运行并引导初始化。

### 5. 在 Obsidian 中打开（可选）

想要图谱视图和双链：打开 Obsidian → 「打开文件夹作为仓库」→ 选择对应目录。

---

## v2 的改进

- **架构精简** — 统一的 `CLAUDE.md` 替代原来的 AGENTS.md + PROCEDURES.md
- **双模式惊奇检测** — 后台模式（别打断）+ 批量模式（标定校准）
- **差异化同步** — 周一到三快速扫描，周四到日深度溯源
- **搭档碰头** — 启动时自然对话，而不是系统报告
- **记忆毕业** — 稳定洞见自动从工作层晋升到长期层
- **完整中文本地化** — `zh-CN/` 目录包含独立的中文区域结构

---

## 文档

- [方法论详解](zh-CN/方法论详解.md) — Personal Agent 范式的完整设计逻辑
- [快速上手](zh-CN/快速上手.md) — 分步骤的配置教程
- [贡献指南](CONTRIBUTING.md) — 如何扩展或定制 Memory Work

## 设计哲学

1. **你提供焦点，AI 提供结构** — 不是你适应工具，是工具适应你
2. **本地优先** — 数据留在你的机器，纯 Markdown 文件
3. **惊奇度驱动** — 只记真正新的东西
4. **周节奏** — 时间边界保护你的注意力
5. **可进化** — 系统和你一起成长，而不是对抗你

## 技术栈

- **Claude** — AI 运行时（通过 Cowork 或 Claude Code）
- **Obsidian** — 知识库 UI（可选但推荐）
- **Markdown** — 所有配置都是可读、可版本控制的文本
- **Git** — 跟踪你的记忆演变历程

没有黑盒平台，没有厂商锁定。一切可迁移。

## 需求

- [Claude Code](https://claude.ai) 或 Claude Desktop with Cowork
- [Obsidian](https://obsidian.md)（可选，用于图谱视图）
- **语音输入工具**（推荐）：[Typeless](https://www.typeless.com/)，或系统自带语音输入

---

## 灵感来源

- [Titans: Learning to Memorize at Test Time](https://arxiv.org/abs/2501.00663)
- [MemSkill: Transferrable and Evolvable Memory Skill Library](https://arxiv.org/abs/2501.03313)
- 管理 10+ 并行项目的真实实践

## 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)。欢迎新技能、翻译和改进。

## 许可证

MIT — 见 [LICENSE](LICENSE)

---

<div align="center">

**你不需要记住一切，你只需要专注于当下。**

由 [@yiliqi78](https://github.com/yiliqi78) 创建

</div>

---

<br>

<div align="center">

# Memory Work v2 (English)

**A Personal Agent architecture for human-AI collaborative knowledge work.**

[中文](#memory-work-v2) | English

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude](https://img.shields.io/badge/Built%20for-Claude-blueviolet)](https://claude.ai)
[![Obsidian](https://img.shields.io/badge/Works%20with-Obsidian-purple)](https://obsidian.md)

</div>

> Your AI doesn't need to be smarter. It needs to remember.

---

## The Problem

When you're juggling 10+ parallel projects, traditional AI assistants make things worse:

- **AI amnesia**: Every conversation starts from scratch. You repeat context endlessly.
- **You become the bottleneck**: Ideas → *you* structure → *you* input → *you* maintain
- **Knowledge base becomes burden**: The bigger it gets, the harder to manage

## The Solution

**Memory Work** flips the script:

- Ideas → **just dictate** → AI structures → AI maintains
- AI reads layered files at startup → **no more amnesia**
- Zone-based agents → **scales to any vault size**

**You only do two things: provide attention focus, make creative decisions.**

AI handles the rest: integrating history, matching materials, structured output.

---

## How It Works

### First Run: Smart Initialization

Clone the repo, open in Claude Code or Cowork, and the AI automatically:

```
1. Detects it's a fresh installation
2. Asks your preferred language (中文 / English)
3. Collects your basic info to create your profile
4. Creates your first week's workspace
5. Asks: "What do you want to work on this week?"
```

**You don't configure anything manually.** Just talk.

<div align="center">

![First Run Demo - Language Selection](docs/images/first-run-demo.png)
*Step 1: Language selection and file initialization*

![First Run Demo - User Setup](docs/images/user-setup-demo-v2.png)
*Step 2: Voice-first user profile configuration*

</div>

### Daily Usage: Voice-First Workflow

```
You: "This week I need to finish the proposal, prep for Wednesday's
     client meeting, and that partnership agreement needs follow-up."

Claude:
1. Breaks into 3 tasks, writes to _this_week.md
2. Searches your vault for related materials
3. Asks you to clarify uncertainties
4. Proactively asks: "Want me to generate a calendar file?"
```

You dictate naturally. Claude structures. **Your flow state stays protected.**

### Weekly Rhythm

```
Monday          →        Mid-week        →         Friday
   │                        │                        │
   ▼                        ▼                        ▼
┌─────────┐           ┌─────────┐            ┌─────────┐
│ Dictate │           │ Progress│            │ Archive │
│   ↓     │           │   ↓     │            │   ↓     │
│AI struct│ ────────▶ │AI assist│ ─────────▶ │AI review│
│   ↓     │           │   ↓     │            │   ↓     │
│Schedule │           │ Output  │            │New week │
└─────────┘           └─────────┘            └─────────┘
```

| Phase | You Do | Claude Does |
|-------|--------|-------------|
| **Monday** | Dictate what you want to do | Structure tasks, pull materials, generate calendar |
| **Mid-week** | Work, add notes anytime | Track progress, search vault, assist decisions |
| **Friday** | Give feedback on memories | Calibrate memory, archive, create next week |

---

## Four-Layer Memory Architecture

The core mechanism that solves AI amnesia. Inspired by [Titans](https://arxiv.org/abs/2501.00663) (surprise-driven) and [MemSkill](https://arxiv.org/abs/2501.03313) (evolvable memory).

| Layer | File | Lifecycle | Purpose |
|-------|------|-----------|---------|
| **Persistent** | SOUL.md, USER.md | Rarely changes | Identity, values, methods |
| **Working** | _this_week.md | Weekly refresh | Current tasks and focus |
| **Dynamic** | MEMORY.md (section) | Cross-week, with decay | Insights, decisions, preferences |
| **Procedural** | MEMORY.md (section) | Accumulate until stable | Behavior patterns, "if X then Y" |

### How Memory Evolves

```
Conversation → AI detects "surprise" → Proposes to remember
                      ↓
          You confirm → Memory saved with metadata
                      ↓
          Weekly review → Calibrate usefulness → Strengthen or decay
```

**Surprise-driven**: Only writes when something deviates from known patterns. No noise.

**User-confirmed**: AI proposes, you approve. Nothing written without consent.

**Has lifecycle**: Strong memories persist (★★★), weak ones fade (★☆☆ → archive after 4 weeks inactive).

**Memory graduation**: Stable patterns auto-promote from MEMORY.md → USER.md as your defining traits.

---

## Focus Zone: Your Attention Anchor

The `00 Focus Zone/` is the heart of the system:

```
00 Focus Zone/
├── _this_week.md      ← Your current attention focus
├── MEMORY_LOG.md      ← Memory system's own journal
├── ITERATION_LOG.md   ← Architecture evolution log
└── _archive/          ← Past weeks
```

<div align="center">

![Focus Zone in Obsidian](docs/images/obsidian-focus-zone-demo.png)
*Complete Focus Zone structure in Obsidian*

</div>

**One week, one file.** Archive on Friday, fresh start on Monday. You never manage the backlog — it's always archived and searchable.

---

## Architecture Overview (v2)

```
memory-work/
├── CLAUDE.md              # System entry point (auto-injected by Cowork)
├── SOUL.md                # AI personality & collaboration style
├── USER.md                # Your profile & stable preferences
├── MEMORY.md              # Long-term memory (Dynamic + Procedural)
│
├── 00 Focus Zone/         # Weekly workspace (working memory)
│   ├── _this_week.md
│   ├── MEMORY_LOG.md
│   ├── ITERATION_LOG.md
│   └── _archive/
│
├── 01 Materials/          # Personal archives (with sensitivity levels)
├── 02 Tools/              # Prompt templates & reusable frameworks
├── 06 Skills/             # Custom AI capabilities
│
├── docs/                  # Documentation & screenshots
├── templates/             # Starter templates
│
└── zh-CN/                 # 完整中文版 (Full Chinese version)
    ├── CLAUDE.md
    ├── SOUL.md, USER.md, MEMORY.md
    ├── 00 专注区/
    ├── 01 你的项目/
    ├── 02 你的阅读/
    └── 03 你的写作/
```

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yiliqi78/memory-work.git
```

Or download: [Download ZIP](https://github.com/yiliqi78/memory-work/archive/refs/heads/main.zip)

### 2. Choose Your Language

- **中文**: Use the `zh-CN/` directory
- **English**: Use the root directory directly

### 3. Open in Claude Code / Cowork

```bash
cd memory-work    # or: cd memory-work/zh-CN
claude .
```

### 4. Start Talking

Send any message (e.g., "Start", "Let's begin"). Claude auto-detects first run and guides initialization.

### 5. Open in Obsidian (Optional)

For graph view and wiki-links: Open Obsidian → "Open folder as vault" → Select the directory.

---

## What's New in v2

- **Architecture Slimming** — Unified `CLAUDE.md` replaces separate AGENTS.md + PROCEDURES.md
- **Dual-Mode Surprise Detection** — Background mode (don't interrupt) + Batch mode (calibrate)
- **Lightweight vs Deep Sync** — Mon–Wed quick scan; Thu–Sun full retrospective
- **Partner Greeting** — Natural startup conversation instead of system report
- **Memory Graduation** — Stable insights auto-promote from working memory to long-term
- **Full Chinese Localization** — Complete `zh-CN/` with localized zone structure

---

## Documentation

- [Methodology Deep-Dive](docs/methodology.md) — The Personal Agent paradigm and design rationale
- [Quick Start Guide](docs/QUICKSTART.md) — Step-by-step initialization walkthrough
- [Contributing Guide](CONTRIBUTING.md) — How to extend or adapt Memory Work

## Design Philosophy

1. **You provide focus, AI provides structure** — Don't adapt to the tool; the tool adapts to you
2. **Local-first** — Your data stays on your machine, plain Markdown files
3. **Surprise-driven** — Only remember what's genuinely new
4. **Weekly rhythm** — Time boundaries protect your attention
5. **Evolvable** — System grows with you, not against you

## Tech Stack

- **Claude** — AI runtime (via Cowork or Claude Code)
- **Obsidian** — Knowledge base UI (optional but recommended)
- **Plain Markdown** — All configuration is readable, versionable text
- **Git** — Track your memory evolution over time

No closed platforms. No vendor lock-in. Everything portable.

## Requirements

- [Claude Code](https://claude.ai) or Claude Desktop with Cowork
- [Obsidian](https://obsidian.md) (optional, for graph view)
- **Voice input tool** (recommended): [Typeless](https://www.typeless.com/), system speech-to-text, or similar

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). We welcome new skills, translations, and improvements.

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">

**You don't need to remember everything. You just need to focus on now.**

Created by [@yiliqi78](https://github.com/yiliqi78)

</div>
