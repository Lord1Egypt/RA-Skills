# kids-points-v2 📊

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-blue)](https://clawhub.ai/cowboy231/skills/kids-points-v2)

简单、可靠的儿童积分管理工具，让家长通过 IM（飞书）和孩子对话式记账。

> **V2** 相比 [kids-points 1.x](https://clawhub.ai/cowboy231/skills/kids-points) 做了全面重构：记账稳定性、CLI 对接能力、轻量化都大幅提升。

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 📊 **SQLite 存储** | 账本从文本文件迁移到 SQLite，并发/断电不再丢数据 |
| 🤖 **LLM 语义分析** | 用大模型提取积分意图，对口语化、方言、不同家庭说法适应性更强（V1 是关键词匹配） |
| 🛠️ **CLI 接口** | 新增 `cli.py`，方便对接 Agent、脚本、外部程序、硬件 |
| 🪶 **更轻** | 剥离 ASR（语音转写），复用飞书自带的转语音功能 |
| 💬 **飞书全量** | 群聊 + 单聊 都支持 |
| 🔁 **防重复** | 基于 messageId 自动去重 |

---

## 🎯 使用方式

直接给飞书 bot 发自然语言就行，比如：

```
今天完成了汉字抄写 2 课，口算题卡 2 篇全对
积分消费 买零食花了 20 分
现在多少分？
今日积分
```

Bot 会自动识别语意 + 记账 + 回报结果。

---

## 🛠️ CLI 接口

V2 暴露了一个 Python CLI，方便 Agent 或外部程序调用：

```bash
# 走完整 8 步 pipeline（LLM 识别 + 记账 + 返 reply）
python3 cli.py "今天数学加 1 分"

# 查余额（不走 LLM）
python3 cli.py balance

# 今日积分
python3 cli.py today

# 历史记录
python3 cli.py history
```

退出码：`0` 成功 / `1` 数据库错误 / `2` 参数错误。

> **⚠️ 重要**：`cli.py` 配合任何消息参数 = 真实写库。**严禁**把 `cli.py "测试..."` 当 dry-run。

---

## 📦 架构概览

```
飞书消息
  ↓
OpenClaw skill dispatch
  ↓
kids-points-v2 handler (handle_feishu_message)
  ↓ subprocess
V2 runtime (cli.py 8 步 pipeline)
  ↓ 写 SQLite (data/kids_points.db)
reply → 飞书
```

**职责分工**：
- **Agent (LLM)**：上游自然语言路由（OpenClaw 平台层）
- **kids-points-v2 skill**：确定性记账 + 防重复 + 数据持久化
- **SQLite**：唯一数据源

---

## 🚀 安装

### ClawHub 安装（推荐）

```bash
clawhub install kids-points-v2
```

安装后默认用 skill 内嵌的 runtime（`skills/kids-points-v2/runtime/`），开箱即用。

### LLM 配置

复制示例配置并填入你的 LLM 信息：

```bash
cd skills/kids-points-v2/runtime
cp config.yaml.example config.yaml
# 编辑 config.yaml，填入你的 api_url / model / key_source
```

`key_source` 推荐用环境变量引用，例如 `env:OPENAI_API_KEY`，然后把 key 放到 shell 环境变量里。

### 自定义 runtime 路径（高级）

如果你想用其他位置的 runtime（比如放在独立项目目录），设环境变量：

```bash
export KIDS_POINTS_RUNTIME_DIR=/path/to/your/kids-points-runtime
```

优先级：`KIDS_POINTS_RUNTIME_DIR` env > skill 内嵌 `runtime/` 默认值。

---

## 📁 文件结构

```
kids-points-v2/                     # 本仓库
├── SKILL.md                        # OpenClaw skill 描述（跟 README 内容对齐）
├── LICENSE                         # MIT
├── README.md                       # GitHub 主页（本文件）
├── .gitignore
├── agent-handler.js                # OpenClaw dispatch 入口
├── scripts/
│   └── handle_feishu.py            # V2 skill handler
└── runtime/                        # V2 Python runtime
    ├── cli.py
    ├── db.py
    ├── pipeline.py
    ├── llm_config.py
    ├── config.yaml.example
    └── data/                       # SQLite 账本位置（.gitignore）
```

---

## 🔌 依赖

- Python 3.8+
- OpenClaw（消息分发）
- LLM API（OpenAI Chat Completions 兼容协议）

---

## 📝 设计原则

1. **数据真实**：积分数据绝不编造，每次操作走真实 SQLite
2. **职责分离**：LLM 只负责语义理解，代码负责数据操作
3. **可追溯**：所有交易记录在 `data/kids_points.db`，可手动查询
4. **可移植**：标准 OpenAI Chat Completions 协议，换模型不改业务逻辑

---

## 🤝 配套项目

- **桌面积分版**（点阵屏硬件展示）：作者另有一个配套硬件项目，将开源到 [github.com/cowboy231](https://github.com/cowboy231)

---

## 📄 License

MIT © [老王](https://github.com/cowboy231)

---

_用心记录每一次进步。_ 🌟