---
name: Polymarket世界杯賠率監控
description: >
  Polymarket世界盃冠軍賠率即時監控。自動掃描100+國家隊市場，追蹤賠率波動>0.5%自動報警。
  適合預測市場套利玩家。
version: 2.0.0
tags: [polymarket, world-cup, prediction-market, monitoring]
license: MIT
author: Vane
payment: 
  model: subscription
  price: $19/month
  method: USDT (Base/Arbitrum)
---

# Polymarket世界盃賠率監控

Polymarket世界盃冠軍賠率即時監控工具。自動掃描100+國家隊冠軍市場，
追蹤賠率波動並發出報警。適合預測市場套利和短線交易。

## 功能

- 自動掃描 Polymarket Gamma API，拉取100+國家隊冠軍市場
- 賠率波動檢測（>0.5%浮動即報警）
- 基線數據對比：記錄每次掃描時的賠率並做diff
- 按成交量排序，自動過濾低流動性市場
- Telegram頻道/群推送警報消息
- 可配置掃描頻率（默認每天2次）

## 輸出示例

```
🇫🇷 France No 83.9% (+0.3%) vol:$38.6M
🇪🇸 Spain Yes 16.5% (-0.5%) vol:$36.2M 🔻
🏴󠁧󠁢󠁥󠁮󠁧󠁿 England Yes 11.0% (-0.3%) vol:$31.7M
```

## 依賴

- Node.js 18+
- 需要代理訪問 Polymarket API

## 安裝

```bash
clawhub install polymarket-worldcup-watcher
openclaw run polymarket-worldcup-watcher
```

## 訂閱

- **價格:** $19/月 (USDT)
- 聯繫 @sgreadybot 開通
