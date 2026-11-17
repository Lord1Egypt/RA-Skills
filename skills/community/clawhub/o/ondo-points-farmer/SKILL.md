---
name: ondo-points-farmer
category: defi
description: Ondo Perps 自动化交易助手 — 在多个高流动性市场执行策略化交易，支持 Points 收益跟踪与预估。面向研究型用户，可配置仓位与轮次，附带收益预估器。
---

# Ondo Points Farmer

> 面向 Ondo Perps 的自动化交易工具：在多个高流动性市场执行策略化交易，同时跟踪交易量对应的 Points 收益。
> Points 由 Ondo Foundation 每周发放，未来可兑换 $ONDO 代币。

## 功能特性

- 支持 10 个高流动性市场：BTC、ETH、SPY、HOOD、AAPL、NVDA、TSLA、QQQ、AMZN、MSFT
- 美股时段自动切换全市场，盘后仅交易 BTC/ETH（24/7 市场）
- 随机化执行：可变间隔、仓位调节、多样化交易方向，避免单一模式
- 交易结束自动清理持仓，输出交易量与成本统计
- 内置 Points 收益预估器，自动校准 pts/$1M 比例，支持持续监控

## 快速开始

### 1. 前置条件

- 注册 [Ondo Perps](https://app.ondoperps.xyz) 账户
- 连接钱包，存入 **≥$50 USDC**（建议 $100）
- 创建 API Key: Settings → API Keys → Create New Key（勾选 Perps Trading）

### 2. 配置环境变量

```bash
export ONDO_KEY_ID="ondoKeyId_你的key_id"
export ONDO_API_SECRET="ondoApiSecret_你的secret"
```

### 3. 运行

```bash
# 默认 $50/轮，~200轮
python3 scripts/farmer.py

# 自定义仓位和轮次
ONDO_POSITION_SIZE=100 ONDO_MAX_CYCLES=500 python3 scripts/farmer.py

# Points 收益预估
python3 scripts/estimator.py

# 持续监控 Points 发放
python3 scripts/estimator.py --watch
```

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `ONDO_KEY_ID` | (必填) | API Key ID |
| `ONDO_API_SECRET` | (必填) | API Secret |
| `ONDO_POSITION_SIZE` | 50 | 每轮名义仓位 ($) |
| `ONDO_MAX_CYCLES` | 200 | 最大循环轮次 |
| `ONDO_MIN_WITHDRAW` | 5 | 自动提现阈值 ($) |

### 支持的市场

- 美股交易时间: BTC, ETH, SPY, HOOD, AAPL, NVDA, TSLA, QQQ, AMZN, MSFT
- 盘后/周末: BTC, ETH（24/7 市场）

## 注意事项

- 实时查询免费（Ondo Perps 公共 API）
- 仅供研究参考，不构成投资建议
- 请遵守平台服务条款，自行承担使用风险

---

*作者 0xcii · 更多工具 https://app.ondoperps.xyz/?ref=8RU3VB*
