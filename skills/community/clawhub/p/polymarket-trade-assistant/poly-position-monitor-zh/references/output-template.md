# 输出模板

## 终端告警格式

```
[HH:MM:SS] 级别 | 类别 | 市场标题
  详细信息
```

示例：
```
[14:32:05] CRITICAL | 价格波动 | Bitcoin 跌至 $60K
  240m 价格变化 -22.3% (阈值 20%), 价格: 0.4050 → 0.3150
[14:32:05] ALERT | 监控地址活动 | 共和党控制众议院
  [GCR] BUY 5000 份 @ 0.1400 ($700)
[14:32:06] WARNING | 成交量异动 | Anthropic 最佳 AI 模型
  成交量暴涨: $12500 (均值 $3200, 倍率 3.9x)
[14:32:06] INFO | 系统
  监控 3 个市场, 5 个仓位
```

## Telegram 消息格式

```
🔴 *CRITICAL* | 价格波动
市场: Bitcoin 跌至 $60K
240m 价格变化 -22.3% (阈值 20%), 价格: 0.4050 → 0.3150
当前价格: 0.3150
变化: -22.30%
阈值: 20%

_2026-02-24 14:32:05 UTC_
```

## 邮件主题格式

```
[Polymarket CRITICAL] 价格波动 - Bitcoin 跌至 $60K
```

## 状态快照 (monitor-state.json)

```json
{
  "timestamp": "2026-02-24T14:32:05+00:00",
  "timestamp_unix": 1740403925,
  "positions": {
    "0xAddress": [
      {
        "market_id": "0x...",
        "asset_id": "12345...",
        "title": "Bitcoin 跌至 $60K?",
        "outcome": "Yes",
        "size": 575,
        "avg_price": 0.43,
        "current_value": 232.3,
        "cur_price": 0.405
      }
    ]
  },
  "orders": [],
  "price_data": {
    "0x...": {
      "current_price": 0.405,
      "current_time": 1740403800
    }
  },
  "volume_data": {
    "0x...": {
      "interval_volume_usd": 5200,
      "total_volume_usd": 85000,
      "total_trades": 142
    }
  },
  "markets": {
    "0x...": {
      "condition_id": "0x...",
      "asset_id": "12345...",
      "title": "Bitcoin 跌至 $60K?",
      "event_slug": "bitcoin-60000-february"
    }
  }
}
```

## 初始持仓快照 (fetch_positions.py 输出)

```
[INFO] Fetching positions for 0x12345...
[INFO]   3 active positions (5 total)

{
  "positions": {"0x...": [...]},
  "monitored_markets": {"condition_id": {...}},
  "total_positions": 3,
  "total_markets": 3
}
```
