---
name: mempalace-openclaw
description: "MemPalace memory system for OpenClaw/XClaw/WorkBuddy. Archive AI conversations to local long-term storage with semantic search. Commands: /mem-arc (archive), /mem-sea (search), /mem-asave (auto-save daily). Based on https://github.com/milla-jovovich/mempalace. Triggers: user wants to save, search or back up AI conversation memories."
---

# MemPalace — AI Long-Term Memory Archive

> **Based on / 基于:** [milla-jovovich/mempalace](https://github.com/milla-jovovich/mempalace)

---

## 总览 / Overview

MemPalace 是一个**本地长期记忆系统**，为 AI 设计。对话永久存档，支持语义搜索。

MemPalace is a **local long-term memory system** for AI agents. Conversations are permanently archived and searchable by meaning (semantic search), not just keywords.

---

## 核心优势 / Key Advantages

| 优势 / Advantage | 说明 / Description |
|-----------------|-------------------|
| 本地存储 / Local Only | 所有数据存在你自己电脑，不上传任何服务器 / All data stays on your machine, nothing uploaded |
| 语义搜索 / Semantic Search | 按意思搜索，不只是关键词匹配 / Searches by meaning, not just keyword match |
| 零费用 / 100% Free | 无需 API Key，无需付费 / No API key, no subscription |
| 跨项目 / Cross-Project | 对话存档跨项目共享，不是单一 workspace / Archives shared across projects, not tied to one workspace |
| 自动归档 / Auto-Archive | 每天 23:00 自动保存，无需手动 / Daily auto-save at 23:00, no manual work |
| 源码内置 / Bundled Source | MemPalace 完整源码打包在 skill 内，首次运行自动安装 / Full MemPalace source bundled, auto-installed on first run |

---

## 费用对比 / Cost Comparison

| 方案 / Solution | 费用 / Cost | 数据位置 / Data Location |
|----------------|------------|------------------------|
| MemPalace | 免费 / Free | 本地 / Local |
| 普通 memory/ | 免费 / Free | workspace 内 / In workspace |
| 第三方云记忆服务 / Cloud memory services | 付费订阅 / Paid | 云端 / Cloud |

---

## 三个命令 / Three Commands

| 命令 / Command | 中文作用 | English Action |
|---------------|---------|--------------|
| `/mem-arc` | 手动归档当前对话到 MemPalace | Archive current session to MemPalace |
| `/mem-sea` | 语义搜索历史记忆 | Semantic search past memories |
| `/mem-asave` | 立即执行今日自动保存 | Auto-save today's memories now |

---

## 工作原理 / How It Works

MemPalace 将对话存储在分级结构中（Wing 主题 > Room 房间 > Drawer 抽屉），通过 ChromaDB 向量数据库实现语义搜索。

MemPalace stores conversations in a hierarchical structure (Wing topic > Room > Drawer) with a ChromaDB vector database for semantic search.

1. Skill 安装后，第一次运行 `/mem-arc` 时自动触发初始化
2. 自动安装 MemPalace 源码 + chromadb/pyyaml 依赖
3. 自动创建 `palace_data/` 目录和 `mempalace.yaml` 配置文件
4. 对话归档时：压缩内容 -> 写入 convos 文件夹 -> 索引到 ChromaDB
5. 搜索时：通过向量匹配找到最相关的记忆片段

---

## 自动配置 / Auto-Setup

第一次运行时自动执行以下步骤，无需手动操作：

1. `pip install -e ./mempalace --no-deps` — 从内置源码安装 mempalace
2. `pip install chromadb pyyaml` — 安装运行时依赖（chromadb 从 PyPI 下载）
3. 创建 `palace_data/` 目录 — 存放对话归档和向量索引
4. 创建 `mempalace.yaml` — Wing 和 Room 配置文件
5. 运行初次索引 — `mempalace mine ./palace_data --wing openclaw`

安装后只需要用命令，无需任何手动配置。

---

## 数据存储位置 / Storage Locations

所有路径相对于 skill 目录，不暴露用户路径。

All paths are relative to the skill directory — no user paths exposed.

mempalace/                    Skill 目录
├── mempalace/                内置 MemPalace 源码
│   ├── cli.py, miner.py     等所有源码文件
│   └── pyproject.toml       pip install -e 所需
├── scripts/
│   └── archive.ps1          归档和搜索脚本
├── palace_data/              首次运行后自动创建
│   ├── convos/              归档的对话文件
│   └── .mempalace/           ChromaDB 向量索引
├── mempalace.yaml            Wing/Room 配置
└── SKILL.md

---

## 适用 AI / Compatible AI

| AI 产品 / AI Product | 支持情况 / Support | 说明 / Notes |
|---------------------|-------------------|------------|
| **OpenClaw** | 完全支持 / Full | Skill 系统 + exec + cron 完整支持 |
| **XClaw** | 待确认 / Unconfirmed | 取决于 exec 工具是否可用 |
| **WorkBuddy** | 待确认 / Unconfirmed | 取决于 exec 工具是否可用 |
| **Claude Code** | 可用 / Usable | 通过 exec 调用 Python/powershell |
| **其他 Agent** | 可用 / Usable | 任何能运行 Python + 脚本的环境 |

Skill 触发机制（description 匹配）是 OpenClaw 特有的。XClaw/WorkBuddy 如果支持 Skill 加载则可用，否则需要手动执行 `scripts/archive.ps1`。

---

## 归档流程 / Archive Flow

1. 读取当前 workspace 的 `memory/` 文件夹内容（或直接传入内容）
2. 压缩：删除问候等废话，保留决策/配置/待办
3. 写入：`palace_data/convos/YYYY-MM-DD-archive.md`
4. 索引：`mempalace mine ./palace_data --wing openclaw`

---

## 搜索流程 / Search Flow

1. 运行：`mempalace search "搜索词" --wing openclaw`
2. ChromaDB 返回向量相似度排序结果
3. AI 解析结果，返回最相关的记忆片段

---

## 主动坦白 / Honest Disclosure

Security Scan 提出了几个合理问题，这里主动说明：

**1. 数据写入位置 / Data Write Location**
archive.ps1 在调用 mempalace CLI 前设置环境变量 `MEMPALACE_PALACE_PATH=palace_data` 目录的绝对路径。所有 MemPalace 数据（对话归档、ChromaDB 向量索引）都写入 skill 目录下的 `palace_data/` 文件夹，不写入用户 home 目录。

**2. Wikipedia 查询 / Wikipedia Lookups**
entity_registry 模块在实体消歧时会发起 Wikipedia API 请求（ benign outbound HTTP，用于消歧，不上传用户数据）。如需完全离线，可注释掉相关代码。

**3. pip install 修改 Python 环境 / pip install Modifies Python Env**
首次运行会执行 `pip install -e ./mempalace` 和 `pip install chromadb pyyaml`，会写入系统 Python 环境。如需隔离，建议用 venv：`pip install -e ./mempalace --no-deps` + `pip install chromadb pyyaml` 可在 venv 中运行。

**4. cron 自动归档 / Cron Auto-Archive**
每天 23:00 的自动归档通过 OpenClaw 内置 cron 实现（`cron add`），属于 OpenClaw 运行时调度，不体现在 skill 代码文件中。如需确认 cron 是否生效，问 AI：`cron list`。

**5. 目录扫描范围 / Directory Scan Scope**
`mempalace mine` 会递归扫描指定目录并索引其中的 .py/.json/.md/.yaml 等文件。归档时请确保 memory/ 目录内无敏感文件，或在归档前由 AI 过滤。

---

*Skill: mempalace-openclaw | Based on milla-jovovich/mempalace | https://github.com/milla-jovovich/mempalace*
