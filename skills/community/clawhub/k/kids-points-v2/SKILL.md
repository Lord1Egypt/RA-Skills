---
name: kids-points-v2
version: 2.0.7
description: 儿童积分管理 V2 - SQLite 存储 + LLM 语义分析 + CLI 接口，飞书群聊与单聊全量支持
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["python3"]}}}
tags: [kids, points, family, sqlite, llm, feishu, chinese, parenting]
---

# kids-points-v2 - 积分助手 V2 📊

简单、可靠的儿童积分管理工具。**V2** 相比 1.x 版本做了全面重构：记账稳定性、CLI 对接能力、轻量化都大幅提升。

---

## ✨ V2 核心特性

| 特性 | 说明 |
|------|------|
| 📊 **SQLite 存储** | 账本从文本文件迁移到 SQLite，并发/断电不再丢数据 |
| 🤖 **LLM 语义分析** | 用大模型提取积分意图，对口语化、方言、不同家庭说法适应性更强 |
| 🛠️ **CLI 接口** | 新增 `cli.py`，方便对接 Agent、脚本、外部程序 |
| 🪶 **更轻** | 剥离 ASR（语音转写），复用飞书自带转写 |
| 💬 **飞书全量** | 群聊 + 单聊 都支持 |
| 🔁 **防重复** | 基于 messageId 自动去重 |

---

## 🎯 使用方式

直接给飞书 bot 发自然语言就行：

```
今天完成了汉字抄写 2 课，口算题卡 2 篇全对
积分消费 买零食花了 20 分
现在多少分？
今日积分
```

Bot 会自动识别语意 + 记账 + 回报结果。

---

## 🛠️ CLI 接口

```bash
# 走完整 8 步 pipeline（LLM 识别 + 记账 + 返 reply）
python3 runtime/cli.py "今天数学加 1 分"

# 查余额（不走 LLM）
python3 runtime/cli.py balance

# 今日积分
python3 runtime/cli.py today

# 历史记录
python3 runtime/cli.py history
```

退出码：`0` 成功 / `1` 数据库错误 / `2` 参数错误。

---

## 📁 项目结构

```
kids-points-v2/
├── runtime/                  # V2 Python runtime（核心逻辑）
│   ├── cli.py                # CLI 入口
│   ├── db.py                 # SQLite 操作层
│   ├── pipeline.py           # 8 步处理 pipeline
│   ├── llm_config.py         # LLM 配置单入口
│   ├── config.yaml.example   # 配置模板（复制为 config.yaml 使用）
│   └── data/                 # SQLite 账本位置
├── skill/                    # OpenClaw skill 包装层
│   ├── SKILL.md
│   ├── agent-handler.js      # OpenClaw dispatch 入口
│   ├── build.sh              # ClawHub 发布打包
│   └── scripts/
│       └── handle_feishu.py  # V2 skill handler
├── extensions/               # 扩展项目（点阵屏看板等）
├── docs/                     # 内部文档
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🔌 依赖

- Python 3.8+
- OpenClaw（消息分发）
- LLM API（OpenAI Chat Completions 兼容协议）

---

## 🚀 安装与配置

### 配置 LLM

复制示例配置并填入你的信息：

```bash
cp runtime/config.yaml.example runtime/config.yaml
# 编辑 config.yaml，填入 api_url / model / key_source
```

`key_source` 推荐用环境变量引用，例如 `env:OPENAI_API_KEY`，然后把 key 放到 shell 环境变量里。

### 自定义 runtime 路径（高级）

如果你想用其他位置的 runtime，设环境变量：

```bash
export KIDS_POINTS_RUNTIME_DIR=/path/to/your/kids-points-runtime
```

优先级：`KIDS_POINTS_RUNTIME_DIR` env > 项目根内嵌 `runtime/` 默认值。

---

## ⚠️ 已知行为

| 输入 | 行为 |
|------|------|
| 浮点积分（如 `0.5`） | 返引导文案，不记账 |
| 模糊短消息 | 返引导文案，提示明确金额 |
| 多笔混合（收入+支出） | 一条 message 处理多笔，写库 |
| 整数加减 | 正常记账 |

---

## 📦 分支说明

| 分支 | 内容 | 用途 |
|------|------|------|
| **main** | 开源安全版（`config.yaml.example` + 产品代码） | GitHub 主分支、ClawHub 发布 |
| **dev** | 自用版（真实配置 + 内部资料 + 测试数据） | 本地开发，不推送 |

开发者：日常在 `dev` 分支 work，定期 merge 到 `main` 后 push。

---

## 📦 配套项目

- 桌面积分版（点阵屏硬件展示）：在 `extensions/` 目录

---

_用心记录每一次进步。_ 🌟

---

## 🌐 English Summary

**Kids Points V2** is a lightweight, reliable family-points tracker that lives in your Feishu (Lark) chat. Send a natural-language sentence — "completed 2 Chinese copybook pages, got all math flashcards right" — and the bot extracts intent, writes to a SQLite ledger, and replies with the result.

**Why V2 (vs. the 1.x line)**

- **SQLite storage** replaces plain-text ledgers: concurrent writes and power-loss no longer corrupt the book.
- **LLM-based intent parsing** via `llm_config.py` adapts to colloquial Chinese, regional phrasing, and each family's wording, instead of brittle regexes.
- **CLI-first**: `runtime/cli.py` exposes `balance` / `today` / `history` and the full pipeline, so agents, cron jobs, and shell scripts can drive the ledger without going through OpenClaw.
- **Feishu full coverage**: group chats *and* direct messages — V1 was DMs only.
- **Deduplication by `messageId`**: idempotent under retries and replays.
- **Lighter footprint**: ASR/TTS is delegated to Feishu itself, so the skill no longer ships an embedded voice pipeline.

**Install (3 steps)**

```bash
cp runtime/config.yaml.example runtime/config.yaml   # then fill in api_url / model / key_source
clawhub install kids-points-v2
# Configure your OpenClaw dispatch to route Feishu messages to the skill handler
```

**CLI quick reference**

```bash
python3 runtime/cli.py "added 1 point for math today"   # full pipeline
python3 runtime/cli.py balance                          # current balance (no LLM)
python3 runtime/cli.py today                            # today's earnings
python3 runtime/cli.py history                          # recent ledger entries
```

Exit codes: `0` success / `1` database error / `2` argument error.

**Requirements**: Python 3.8+, OpenClaw for Feishu dispatch, any LLM API speaking the OpenAI Chat Completions protocol.

See `README.en.md` in the repository for the full English README, including the optional HUB75 LED-matrix dashboard extension under `extensions/`.
