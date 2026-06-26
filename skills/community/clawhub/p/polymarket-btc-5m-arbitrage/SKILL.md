---
name: polymarket-btc-5m-arbitrage
description: Polymarket BTC 5分钟高频套利机器人 - 自动交易BTC涨跌预测市场，支持 SkillPay 计费
version: 1.0.1
---

# Polymarket BTC 5分钟套利机器人

自动交易 Polymarket BTC 5分钟涨跌预测市场（btc-up-or-down-5m系列）

## 功能

- 自动发现当前和即将到来的5分钟BTC市场
- 实时订单簿分析
- 价差套利交易
- 支持限价单和市价单
- 自动做市提供流动性
- **支持 SkillPay 计费** (可选)

## 使用方法

### 1. 配置

设置环境变量或 config.json:
```bash
export POLYMARKET_PRIVATE_KEY="your_private_key"
export POLYMARKET_API_KEY="your_api_key"
export SKILLPAY_API_KEY="your_skillpay_key"  # 可选
```

### 2. 运行

```bash
python3 scripts/polymarket_btc_5m_bot.py
```

### 3. 可选参数

```bash
python3 scripts/polymarket_btc_5m_bot.py --help
```

## 市场信息

- **系列**: btc-up-or-down-5m
- **类型**: 5分钟BTC涨跌预测
- **分辨率**: Chainlink BTC/USD
- **交易对**: Up/Down

## API

- Gamma API: https://gamma-api.polymarket.com
- CLOB API: https://clob.polymarket.com

## SkillPay 计费

本 Skill 支持 SkillPay 计费系统（可选）：
- 用户需先支付才能使用
- 未支付时返回支付链接
- 开发者可获得 95% 收入

详细见: https://skillpay.me

## 参考

- `references/api-reference.md` - API 详细文档
- `references/trading-strategy.md` - 交易策略说明
