---
name: polymarket-autotrade
description: Polymarket prediction market CLI - Browse markets, check prices, execute trades, and manage portfolio.
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - POLYMARKET_PRIVATE_KEY
        - POLYMARKET_PROXY_ADDRESS
      bins:
        - python3
        - pip
    primaryEnv: POLYMARKET_PRIVATE_KEY
    emoji: "📈"
    install:
      - kind: uv
        package: requests
        bins: []
      - kind: uv
        package: py-clob-client
        bins: []
    os:
      - linux
      - macos
---

# polymarket

Polymarket prediction market CLI - Browse & Trade.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt
```

### Configure credentials

**Method 1: Via `openclaw.json` (Recommended)**

Add to your `~/.openclaw/openclaw.json` under `skills.entries`:

```json
{
  "skills": {
    "entries": {
      "polymarket": {
        "env": {
          "POLYMARKET_PRIVATE_KEY": "your_wallet_private_key",
          "POLYMARKET_PROXY_ADDRESS": "0x_your_proxy_wallet_address"
        }
      }
    }
  }
}
```

Or use the shorthand `apiKey` field for the primary key:

```json
{
  "skills": {
    "entries": {
      "polymarket": {
        "apiKey": "your_wallet_private_key",
        "env": {
          "POLYMARKET_PROXY_ADDRESS": "0x_your_proxy_wallet_address"
        }
      }
    }
  }
}
```

**Method 2: Via config file (Legacy)**

Create `~/.openclaw/credentials/polymarket.json`:

```json
{
  "private_key": "your_wallet_private_key",
  "proxy_address": "0x_your_proxy_wallet_address"
}
```

> The skill checks env vars first, then falls back to the config file.

**Credential details:**
- `POLYMARKET_PRIVATE_KEY` / `private_key` — Your wallet private key (from MetaMask or similar)
- `POLYMARKET_PROXY_ADDRESS` / `proxy_address` — Your Polymarket proxy wallet address (from polymarket.com/settings)
- API credentials (`apiKey`, `secret`, `passphrase`) are **auto-generated** on first trade and cached locally.

### Security Warning

- **Strongly recommended**: Use a **dedicated wallet with limited funds**, NOT your main wallet.
- The private key is **only used locally** for signing transactions via `py-clob-client`. It is **never transmitted** to any endpoint other than `clob.polymarket.com` (Polymarket's official CLOB API).
- If using config file method: `chmod 600 ~/.openclaw/credentials/polymarket.json`

## Commands

### Browse Markets
```bash
polymarket trending                     # Homepage (featured order)
polymarket trending geopolitics          # By category
polymarket trending crypto
polymarket trending sports
polymarket trending politics
polymarket trending business
polymarket trending entertainment
polymarket trending tech
```

### Event Details
```bash
polymarket detail us-strikes-iran-by
polymarket event us-strikes-iran-by     # Simple overview
```

### Trading
```bash
# Check price
polymarket price <token_id>

# Trade (requires credentials)
polymarket buy <token_id> <amount>     # Buy with USDC
polymarket sell <token_id> <amount>    # Sell USDC worth

# Example
polymarket buy 40081275558852222228080198821361202017557872256707631666334039001378518619916 2
```

### Portfolio
```bash
polymarket position                     # From config wallet
polymarket position <wallet_address>
polymarket balance                    # From config wallet
polymarket balance <wallet_address>
```

## Natural Language Triggers

### Browse Markets
> "Polymarket 有什么热门市场"
> "显示当前趋势"
> "查看政治预测市场"
> "加密货币市场怎么样"
> "体育博彩市场"
> "商业/经济类预测市场"
> "娱乐新闻相关"
> "What's trending on Polymarket"
> "Show me popular prediction markets"

### Event Details
> "2028共和党候选人详情"
> "伊朗战争市场详细信息"
> "J.D. Vance 当前概率多少"
> "这个市场什么意思"
> "Show me details about [event name]"
> "What are the odds for [outcome]"
> "Explain this market"

### Trading
> "买入 J.D. Vance YES"
> "买 2 美元"
> "做多比特币"
> "下注 5 美元"
> "Buy [token/outcome]"
> "I want to buy [amount] USDC of [outcome]"
> "Place a bet on [outcome]"
> "Long [market]"

### Portfolio
> "我的仓位"
> "我的持仓"
> "还剩多少钱"
> "当前余额"
> "My positions"
> "Show me my balance"
> "How much USDC do I have"

## Features

- **Env-first credentials** - Reads `POLYMARKET_PRIVATE_KEY` / `POLYMARKET_PROXY_ADDRESS` from env, falls back to config file
- **Auto API credentials** - Generated on first trade and cached to `~/.openclaw/credentials/polymarket_api.json`
- **Default wallet** - Uses `proxy_address` from config for position/balance commands
- **Local-only signing** - Private key never leaves your machine; only signed transactions are sent to Polymarket CLOB API

## APIs

- Events: https://gamma-api.polymarket.com/events/pagination
- Positions: https://data-api.polymarket.com/positions
- Trading: https://clob.polymarket.com
