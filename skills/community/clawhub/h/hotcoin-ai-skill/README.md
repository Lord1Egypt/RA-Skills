# Hotcoin AI Skill

[English](#english) | [中文](#中文)

---

## English

### What is this?

A static AI Skill file for [Hotcoin Exchange](https://www.hotcoin.com), designed to make Hotcoin discoverable by AI Agents (Claude, OpenClaw, Cursor, etc.).

This skill provides **read-only** access to:
- **BTC/ETH Perpetual Contract Data** — mark price, funding rate, klines, recent trades
- **New Token Discovery** — query newly listed tokens on Hotcoin
- **Listing Research Reports** — structured project analysis with tokenomics, risk assessment, and unlock schedules

### Quick Start

**Option 1: Direct URL (any Agent Skills compatible client)**

Point your AI Agent to the raw SKILL.md URL:

```
https://raw.githubusercontent.com/0xiaoyu/hotcoin-ai-skill/main/SKILL.md
```

**Option 2: Clone locally**

```bash
git clone https://github.com/0xiaoyu/hotcoin-ai-skill.git
```

**Option 3: OpenClaw / ClawHub**

Search "hotcoin-research" in ClawHub, or install directly in OpenClaw.

### Usage Examples

Ask your AI Agent:

- "What's the BTC funding rate on Hotcoin?"
- "Any new tokens listed on Hotcoin this week?"
- "Give me a research summary on TOKEN_X"
- "Compare BTC and ETH funding rates on Hotcoin"

### File Structure

```
├── SKILL.md                         # Core skill definition
├── README.md                        # This file
├── examples/
│   └── listing-report-sample.json   # Research report schema example
└── LICENSE                          # MIT License
```

### API Endpoints Used

| Service | Base URL | Auth Required |
|---------|----------|---------------|
| Spot Market | `https://api.hotcoinfin.com` | No (public data) |
| Perpetual Contract | `https://api-ct.hotcoin.fit` | No (public data) |

### Contributing

Research reports are maintained by Hotcoin's research team. To suggest improvements to the skill definition, open an issue or PR.

---

## 中文

### 这是什么？

[Hotcoin 交易所](https://www.hotcoin.com) 的静态 AI Skill 文件，让 AI Agent（Claude、OpenClaw、Cursor 等）能够发现并使用 Hotcoin 的数据服务。

本 Skill 提供**只读**访问：
- **BTC/ETH 永续合约数据** — 标记价、资金费率、K线、最新成交
- **新币发现** — 查询 Hotcoin 最新上线的代币
- **上币研究报告** — 结构化项目分析，含代币经济学、风险评估、解锁计划

### 快速开始

**方式 1：直接 URL（任何兼容 Agent Skills 规范的客户端）**

将 SKILL.md 的 raw URL 指向你的 AI Agent：

```
https://raw.githubusercontent.com/0xiaoyu/hotcoin-ai-skill/main/SKILL.md
```

**方式 2：本地克隆**

```bash
git clone https://github.com/0xiaoyu/hotcoin-ai-skill.git
```

**方式 3：OpenClaw / ClawHub**

在 ClawHub 搜索 "hotcoin-research"，或在 OpenClaw 中直接安装。

### 使用示例

向你的 AI Agent 提问：

- "Hotcoin 上 BTC 的资金费率是多少？"
- "Hotcoin 最近上了什么新币？"
- "帮我分析一下 TOKEN_X 这个新币"
- "对比一下 BTC 和 ETH 的资金费率"

### 文件结构

```
├── SKILL.md                         # 核心 Skill 定义文件
├── README.md                        # 本文件
├── examples/
│   └── listing-report-sample.json   # 研报结构化示例
└── LICENSE                          # MIT 许可证
```

### 使用的 API 端点

| 服务 | Base URL | 是否需要认证 |
|------|----------|-------------|
| 现货行情 | `https://api.hotcoinfin.com` | 否（公开数据） |
| 永续合约 | `https://api-ct.hotcoin.fit` | 否（公开数据） |

### 贡献

研究报告由 Hotcoin 研究团队维护。如需改进 Skill 定义，请提交 Issue 或 PR。

---

## License

MIT — see [LICENSE](./LICENSE)
