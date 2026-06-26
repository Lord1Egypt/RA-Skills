# pmbuysell Skills — Polymarket Trading for AI Agents

## 功能说明 / Feature Overview

**pmbuysell skills** 是一套面向 AI 智能体的 Polymarket 交易技能包，提供 CLI 命令完成下单、查余额、自动结算和配置管理，包内自包含，不依赖外部业务模块。

**pmbuysell skills** is a Polymarket trading skill pack for AI agents. It provides CLI commands for placing orders, checking balances, auto-redeeming settled positions, and managing config—all self-contained within the package, with no dependency on external business modules.

---

## 核心能力 / Core Capabilities

| 能力 / Capability | 说明 / Description |
|-------------------|--------------------|
| **配置初始化** / Config Init | 一键生成 `pmbuysell/.env` 模板，便于智能体首次使用 / One-command generation of `.env` template for first-time setup |
| **配置校验** / Config Check | 校验账号、私钥、funder 及 redeem 相关凭证是否完整 / Validates account, private key, funder, and redeem-related credentials |
| **市价买卖** / Market Trade | 按 slug + side + amount 市价买入/卖出；支持 5m/15m 自动 slug / Market buy/sell by slug; supports auto slug for 5m/15m buckets |
| **余额查询** / Balance Query | 查询 USDC 余额及指定市场的 up/down 持仓 / Query USDC balance and up/down positions for a given market |
| **自动结算** / Auto Redeem | 付费模块 `pmbuysell_redeem`，需单独安装 / Paid addon `pmbuysell_redeem`, install separately |

---

## 使用入口 / Entry Points

| 命令 / Command | 功能 / Function |
|----------------|-----------------|
| `python -m pmbuysell.skills.init_cli` | 生成 .env 模板 / Generate .env template |
| `python -m pmbuysell.skills.check_config_cli` | 配置校验 / Config validation |
| `python -m pmbuysell.skills.trade_cli` | 下单买卖 / Place market orders |
| `python -m pmbuysell.skills.balance_cli` | 余额/持仓查询 / Balance & position query |
| `python -m pmbuysell.skills.auto_redeem_cli` | 自动结算入口（免费版仅提示购买 Pro）/ Auto redeem entry (free: paywall) |
| `python -m pmbuysell_redeem.cli` | 自动结算（Pro 付费模块）/ Auto redeem (Pro paid addon) |

---

## 发布文案（可直接粘贴）/ Copy-Paste for Marketplace

### 中文

**pmbuysell Skills — Polymarket AI 交易技能包**

面向 AI 智能体的 Polymarket 交易技能，支持多账号、市价买卖、余额查询和自动结算。包内自包含，可独立运行，无需依赖主业务代码。

- 配置初始化与校验
- 市价买入/卖出（支持 5m/15m 自动 slug）
- USDC 余额及市场持仓查询
- 自动结算（redeem）为付费模块 `pmbuysell_redeem`，需单独购买/安装
- 输出 JSON，便于智能体解析

运行环境：在包含 `pmbuysell/` 的项目根目录执行，需配置 `.env` 中的账号、私钥、funder。

---

### English

**pmbuysell Skills — Polymarket Trading Skill Pack for AI Agents**

Polymarket trading skills for AI agents: multi-account support, market buy/sell, balance and position queries, and auto-redeem of settled positions. Self-contained within the package, runs standalone without depending on the main application.

- Config initialization and validation
- Market buy/sell (auto slug for 5m/15m buckets)
- USDC balance and market position queries
- Auto redeem via paid addon `pmbuysell_redeem` (separate install)
- JSON output for easy agent parsing

Run from the project root containing `pmbuysell/`. Requires `.env` with account, private key, and funder configured.
