---
name: polymarket-trade-skills
version: 1.0.2
description: Polymarket 预测市场全链路 AI 交易工具包。包含 13 个 skill，覆盖市场扫描、概率评估、订单簿分析、实盘交易、持仓监控、结算追踪、回测复盘的完整工作流。支持中英双语。当用户提到 Polymarket 交易、预测市场分析、市场脉搏、持仓管理、自动交易时使用。
metadata: {"openclaw": {"emoji": "🎰", "homepage": "https://clawhub.ai/skills/polymarket-trade-skills", "requires": {"bins": ["python3"]}, "envVars": [{"name": "PRIVATE_KEY", "required": false, "description": "Polymarket wallet private key (needed for trading skills only)"}, {"name": "FUNDER_ADDRESS", "required": false, "description": "Polymarket funder/proxy wallet address (needed for trading skills only)"}]}}
---

# Polymarket Trade Skills

全链路 Polymarket 预测市场 AI 交易工具包，一次安装获得 13 个专业 skill。

## 包含的 Skills

| Skill | 触发命令 | 功能 |
|-------|---------|------|
| polymarket-market-pulse | `/polymarket-market-pulse` | 市场扫描与 Top 3 推荐（EN） |
| polymarket-market-pulse-zh | `/polymarket-market-pulse-zh` | 市场扫描与 Top 3 推荐（中文） |
| api-trade-polymarket | `/api-trade-polymarket` | CLOB API 实盘交易执行 |
| polymarket-paper-trading | `/polymarket-paper-trading` | 纸上交易与组合管理 |
| danger-auto-trade-polymarket | `/danger-auto-trade-polymarket` | 全自动交易（无需确认） |
| portfolio-review-polymarket | `/portfolio-review-polymarket` | EV 最大化持仓审查（EN） |
| portfolio-review-polymarket-zh | `/portfolio-review-polymarket-zh` | EV 最大化持仓审查（中文） |
| poly-position-monitor | `/poly-position-monitor` | 实时持仓监控与告警（EN） |
| poly-position-monitor-zh | `/poly-position-monitor-zh` | 实时持仓监控与告警（中文） |
| poly-resolution-tracking | `/poly-resolution-tracking` | 结算数据源追踪（EN） |
| poly-resolution-tracking-zh | `/poly-resolution-tracking-zh` | 结算数据源追踪（中文） |
| back-testing-predmarket | `/back-testing-predmarket` | 推荐回测与绩效评估（EN） |
| back-testing-predmarket-zh | `/back-testing-predmarket-zh` | 推荐回测与绩效评估（中文） |

## 典型工作流

```
扫描机会 → 组合审查 → 下单交易 → 持仓监控 → 结算追踪 → 回测复盘
```

### 日常扫描 + 下单
```
/polymarket-market-pulse-zh    → 获取 Top 3 推荐
/polymarket-paper-trading       → 交互式确认下单
```

### 持仓管理
```
/poly-position-monitor-zh      → 持续监控持仓异动
/portfolio-review-polymarket-zh → 定期审查持仓 EV
/poly-resolution-tracking-zh   → 追踪关键市场结算进度
```

### 全自动（高风险）
```
/danger-auto-trade-polymarket --dry-run  → 模拟全自动交易
/danger-auto-trade-polymarket            → 实盘全自动
```

## 环境要求

- **必需：** Python 3、Node.js（含 npx）
- **交易功能：** 需要 `.env.aizen` 配置文件（含 PRIVATE_KEY、FUNDER_ADDRESS）
- **监控功能：** 可选 Telegram Bot Token + CLOB API 凭证
- **CLI 工具：** `polymarket` CLI（Rust）用于订单簿和评论获取

## 安装

```bash
openclaw skills install polymarket-trade-skills
```
