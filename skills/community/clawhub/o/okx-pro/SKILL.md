---
name: okx-pro
version: 1.0.0
description: 完整 OKX 交易所集成，U本位/币本位合约，杠杆交易，止盈止损，仓位管理
metadata: {"openclaw":{"emoji":"🟧","always":true,"requires":{"bins":["curl","jq","openssl"]}}}
---

# OKX Pro 🟧

专业 OKX 交易所交易技能 - 全球领先的加密货币合约交易所。

## 🚀 Quick Start

### Setup Credentials

Save to `~/.openclaw/credentials/okx.json`:
```json
{
  "apiKey": "YOUR_API_KEY",
  "secretKey": "YOUR_SECRET_KEY",
  "passphrase": "YOUR_PASSPHRASE"
}
```

### Environment Variables (alternative)
```bash
export OKX_API_KEY="your_api_key"
export OKX_SECRET="your_secret_key"
export OKX_PASSPHRASE="your_passphrase"
```

---

# 📖 技术文档 | Technical Documentation

## 中文文档

### 1. 概述

OKX Pro 是一个完整的 OKX 交易所集成技能，支持：
- 现货交易 (Spot Trading)
- 合约交易 (Futures Trading)
- U本位合约 / 币本位合约
- 杠杆交易 (Leverage Trading)
- 止盈止损 (Take Profit / Stop Loss)
- 仓位管理 (Position Management)

### 2. API 版本

本技能使用 OKX V5 API：
- 基础URL: `https://www.okx.com`
- 所有请求需要签名认证

### 3. 支持的交易对

| 交易对 | 说明 |
|--------|------|
| BTC-USDT | BTC 现货 |
| ETH-USDT | ETH 现货 |
| BTC-USDT-SWAP | BTC U本位永续合约 |
| ETH-USDT-SWAP | ETH U本位永续合约 |
| BTC-USD-SWAP | BTC 币本位永续合约 |

### 4. 交易参数

| 参数 | 说明 | 示例 |
|------|------|------|
| instId | 交易对ID | BTC-USDT-SWAP |
| tdMode | 仓位模式 | cross(全仓) / isolated(逐仓) |
| side | 交易方向 | buy / sell |
| ordType | 订单类型 | market / limit / conditional |
| sz | 数量 | 0.001 |
| px | 价格 | 50000 |
| SL | 止损 | slTriggerPx |
| TP | 止盈 | tpTriggerPx |

### 5. 订单类型详解

#### 市价单 (Market Order)
立即以市场价成交
```json
{"instId":"BTC-USDT-SWAP","tdMode":"cross","side":"buy","ordType":"market","sz":"0.001"}
```

#### 限价单 (Limit Order)
指定价格成交
```json
{"instId":"BTC-USDT-SWAP","tdMode":"cross","side":"buy","ordType":"limit","sz":"0.001","px":"50000"}
```

#### 条件单 (Conditional Order)
止盈止损订单
```json
{
  "instId": "BTC-USDT-SWAP",
  "tdMode": "cross",
  "side": "sell",
  "ordType": "conditional",
  "sz": "0.001",
  "slTriggerPx": "45000",
  "slOrdPx": "-1"
}
```

### 6. 止盈止损详解

- `slTriggerPx`: 止损触发价格
- `slOrdPx`: 止损订单价格 (-1 = 市价)
- `tpTriggerPx`: 止盈触发价格
- `tpOrdPx`: 止盈订单价格

### 7. 仓位管理

| 操作 | API |
|------|-----|
| 查询仓位 | GET /api/v5/position/positions |
| 设置杠杆 | POST /api/v5/account/set-leverage |
| 追加保证金 | POST /api/v5/account/increase-margin |
| 减少保证金 | POST /api/v5/account/decrease-margin |

### 8. 风险控制

⚠️ 安全规则：
1. 杠杆不超过10x（新手建议2-3x）
2. 始终设置止损
3. 大额订单先确认
4. 测试网验证后再实盘

---

## English Documentation

### 1. Overview

OKX Pro provides complete OKX exchange integration:
- Spot Trading
- Futures Trading (U-Margin / Coin-Margin)
- Leverage Trading
- Take Profit / Stop Loss
- Position Management

### 2. API Version

Uses OKX V5 API:
- Base URL: `https://www.okx.com`
- All requests require signature authentication

### 3. Supported Trading Pairs

| Pair | Description |
|------|-------------|
| BTC-USDT | BTC Spot |
| ETH-USDT | ETH Spot |
| BTC-USDT-SWAP | BTC USDT-Margin Perpetual |
| ETH-USDT-SWAP | ETH USDT-Margin Perpetual |

### 4. Trading Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| instId | Instrument ID | BTC-USDT-SWAP |
| tdMode | Trade Mode | cross / isolated |
| side | Order Side | buy / sell |
| ordType | Order Type | market / limit / conditional |
| sz | Size | 0.001 |
| px | Price | 50000 |

### 5. Order Types

#### Market Order
Execute immediately at market price
```json
{"instId":"BTC-USDT-SWAP","tdMode":"cross","side":"buy","ordType":"market","sz":"0.001"}
```

#### Limit Order
Execute at specified price
```json
{"instId":"BTC-USDT-SWAP","tdMode":"cross","side":"buy","ordType":"limit","sz":"0.001","px":"50000"}
```

#### Conditional Order
Stop loss / Take profit orders
```json
{
  "instId": "BTC-USDT-SWAP",
  "tdMode": "cross",
  "side": "sell",
  "ordType": "conditional",
  "sz": "0.001",
  "slTriggerPx": "45000",
  "slOrdPx": "-1"
}
```

### 6. Stop Loss / Take Profit

- `slTriggerPx`: Stop loss trigger price
- `slOrdPx`: Stop loss order price (-1 = market)
- `tpTriggerPx`: Take profit trigger price
- `tpOrdPx`: Take profit order price

### 7. Position Management

| Operation | API |
|-----------|-----|
| Get Positions | GET /api/v5/position/positions |
| Set Leverage | POST /api/v5/account/set-leverage |
| Increase Margin | POST /api/v5/account/increase-margin |
| Decrease Margin | POST /api/v5/account/decrease-margin |

### 8. Risk Control

⚠️ Safety Rules:
1. Leverage max 10x (beginners: 2-3x)
2. Always set stop loss
3. Confirm large orders
4. Test on demo trading first

---

## 🔐 Signature Helper

```bash
# 生成 OKX 签名的函数
okx_sign() {
  local method="$1"
  local request_path="$2"
  local body="$3"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")
  local message="${timestamp}${method}${request_path}${body}"
  local signature=$(echo -n "$message" | openssl dgst -sha256 -hmac "$OKX_SECRET" | cut -d' ' -f2)
  echo "$signature"
}

okx_request() {
  local method="$1"
  local endpoint="$2"
  local body="$3"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")
  local signature=$(okx_sign "$method" "$endpoint" "$body")
  
  curl -s -X "$method" "https://www.okx.com$endpoint" \
    -H "Content-Type: application/json" \
    -H "OKX-ACCESS-KEY: $OKX_API_KEY" \
    -H "OKX-ACCESS-SIGN: $signature" \
    -H "OKX-ACCESS-TIMESTAMP: $timestamp" \
    -H "OKX-ACCESS-PASSPHRASE: $OKX_PASSPHRASE" \
    -d "$body"
}
```

## 📊 Basic Queries

### Check Balance
```bash
okx_request "GET" "/api/v5/account/balance" ''
```

### Get Current Price
```bash
curl -s "https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT" | jq '.data[0]'
```

### Get All Positions
```bash
okx_request "GET" "/api/v5/position/positions" ''
```

## ⚡ Futures Trading

### Open LONG Position (Buy)
```bash
INST_ID="BTC-USDT-SWAP"
SZ="0.001"
TD_MODE="cross"

okx_request "POST" "/api/v5/trade/order" "{\"instId\":\"$INST_ID\",\"tdMode\":\"$TD_MODE\",\"side\":\"buy\",\"ordType\":\"market\",\"sz\":\"$SZ\"}"
```

### Open SHORT Position (Sell)
```bash
INST_ID="BTC-USDT-SWAP"
SZ="0.001"
TD_MODE="cross"

okx_request "POST" "/api/v5/trade/order" "{\"instId\":\"$INST_ID\",\"tdMode\":\"$TD_MODE\",\"side\":\"sell\",\"ordType\":\"market\",\"sz\":\"$SZ\"}"
```

### Set Stop Loss
```bash
INST_ID="BTC-USDT-SWAP"
SZ="0.001"
STOP_PRICE="75000"
TD_MODE="cross"

okx_request "POST" "/api/v5/trade/order" "{\"instId\":\"$INST_ID\",\"tdMode\":\"$TD_MODE\",\"side\":\"sell\",\"ordType\":\"conditional\",\"sz\":\"$SZ\",\"slTriggerPx\":\"$STOP_PRICE\",\"slOrdPx\":\"-1\"}"
```

### Set Take Profit
```bash
INST_ID="BTC-USDT-SWAP"
SZ="0.001"
TP_PRICE="85000"
TD_MODE="cross"

okx_request "POST" "/api/v5/trade/order" "{\"instId\":\"$INST_ID\",\"tdMode\":\"$TD_MODE\",\"side\":\"sell\",\"ordType\":\"conditional\",\"sz\":\"$SZ\",\"tpTriggerPx\":\"$TP_PRICE\",\"tpOrdPx\":\"-1\"}"
```

### Close Position (Market)
```bash
INST_ID="BTC-USDT-SWAP"
SZ="0.001"
TD_MODE="cross"

okx_request "POST" "/api/v5/trade/close-position" "{\"instId\":\"$INST_ID\",\"mgnMode\":\"cross\",\"posSide\":\"long\"}"
```

### Set Leverage
```bash
INST_ID="BTC-USDT-SWAP"
LEVERAGE="10"
TD_MODE="cross"

okx_request "POST" "/api/v5/account/set-leverage" "{\"instId\":\"$INST_ID\",\"lever\":\"$LEVERAGE\",\"mgnMode\":\"$TD_MODE\"}"
```

## 📈 Spot Trading

### Buy (Market)
```bash
INST_ID="BTC-USDT"
SZ="0.001"

okx_request "POST" "/api/v5/trade/order" "{\"instId\":\"$INST_ID\",\"tdMode\":\"cash\",\"side\":\"buy\",\"ordType\":\"market\",\"sz\":\"$SZ\"}"
```

### Sell (Market)
```bash
INST_ID="BTC-USDT"
SZ="0.001"

okx_request "POST" "/api/v5/trade/order" "{\"instId\":\"$INST_ID\",\"tdMode\":\"cash\",\"side\":\"sell\",\"ordType\":\"market\",\"sz\":\"$SZ\"}"
```

## 🔧 Utilities

### View Open Orders
```bash
okx_request "GET" "/api/v5/trade/orders-pending" ''
```

### Cancel Order
```bash
INST_ID="BTC-USDT-SWAP"
ORD_ID="123456789"

okx_request "POST" "/api/v5/trade/cancel-order" "{\"instId\":\"$INST_ID\",\"ordId\":\"$ORD_ID\"}"
```

### View Trade History
```bash
okx_request "GET" "/api/v5/trade/fills" ''
```

## 📋 Popular Pairs

| InstID | Description |
|--------|-------------|
| BTC-USDT | Bitcoin U本位合约 |
| ETH-USDT | Ethereum U本位合约 |
| SOL-USDT | Solana U本位合约 |
| XRP-USDT | XRP U本位合约 |
| DOGE-USDT | Dogecoin U本位合约 |
| BTC-USDT-SWAP | 永续合约 |
| ETH-USDT-SWAP | ETH 永续合约 |

## ⚠️ Safety Rules

1. **ALWAYS** verify position before closing
2. **ALWAYS** set Stop Loss on leveraged trades
3. **NEVER** use leverage higher than 10x without experience
4. **VERIFY** pair and quantity before executing
5. **CONFIRM** with user before executing large orders
6. **注意**：U本位合约用 USDT 计价，币本位用 USD/BTC 计价

## 🔗 Links

- [API Documentation](https://www.okx.com/docs-v5/)
- [Create Account](https://www.okx.com/)
- [Testnet](https://www.okx.com/market/trade/demo)
