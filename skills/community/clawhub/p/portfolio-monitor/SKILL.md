---
name: portfolio-monitor
description: 投资组合监控系统。管理股票、加密货币持仓，跟踪成本、盈亏，设置价格提醒，生成组合报告。支持港股、美股、加密货币。
---

# 投资组合监控

管理投资持仓，跟踪盈亏，生成分析报告。

## 快速开始

```bash
pip3 install yfinance --break-system-packages
python3 scripts/portfolio.py
```

## 配置持仓

编辑 `memory/portfolio.json`：
```json
{
  "holdings": [
    {"symbol": "0700.HK", "name": "腾讯", "shares": 100, "cost": 500, "currency": "HKD"},
    {"symbol": "AAPL", "name": "苹果", "shares": 10, "cost": 180, "currency": "USD"},
    {"symbol": "BTC-USD", "name": "比特币", "shares": 0.5, "cost": 45000, "currency": "USD"}
  ]
}
```

## 功能

- ✅ 实时市价
- ✅ 持仓盈亏金额/比例
- ✅ 总组合盈亏
- ✅ 涨跌幅提醒(默认5%)
- ✅ 多币种支持

## 输出示例

```
💰 总资产: $92,475
💵 总成本: $79,300
📈 总盈亏: +$13,175 (+16.62%)

📈 苹果: +43.03% 🔔涨幅超5%
📉 以太坊: -20.69% 🔔跌幅超5%
```

## 提醒阈值

修改 `memory/portfolio.json` 中的 `alert_threshold`:
```json
"settings": {"alert_threshold": 0.05}
```

## 风险提示

⚠️ 仅供记录参考，不构成投资建议。
