---
name: paper-ondo-hedge
description: >
  Use when the user asks to run the PaperTrade + ONDO neutral hedge bot,
  configure hedging parameters, check account status, close all positions,
  or register a PaperTrade Session Key. Also use for loss mining, PAPER token
  farming, or setting up the web control panel.
version: 1.0.0
allowed-tools:
  - Bash(python *)
  - Bash(curl *)
  - Bash(git *)
  - Read
  - Write
metadata:
  openclaw:
    emoji: "⚡"
    homepage: https://github.com/0xcii/paper-ondo-hedge-bot
    requires:
      env:
        - PAPER_WALLET_PRIVATE_KEY
        - PAPER_SESSION_KEY
        - ONDO_KEY_ID
        - ONDO_API_SECRET
        - HEDGE_MODE
        - HEDGE_SYMBOL
        - HEDGE_POSITION_SIZE
        - HEDGE_PAPER_LEVERAGE
        - HEDGE_ONDO_LEVERAGE
        - HEDGE_TARGET_MOVE_PCT
        - HEDGE_MAX_HOLD_SECONDS
        - HEDGE_POLL_INTERVAL
        - HEDGE_MAX_CYCLES
        - HEDGE_DIRECTION
      bins:
        - python3
        - pip
---

# PaperTrade + ONDO Perps 中性对冲机器人

A neutral hedging bot that mines PAPER tokens on PaperTrade while hedging with ONDO Perps.

## When to use

Use this skill when:
- The user wants to run or start the hedge bot
- The user asks to check PaperTrade or ONDO account status
- The user wants to close all positions (emergency)
- The user wants to register a PaperTrade Session Key
- The user wants to adjust hedging parameters (position size, leverage, target move)
- The user wants to launch the web control panel
- The user wants to switch between mock and real mode
- The user asks about loss mining or PAPER token farming on PaperTrade

Do NOT use this skill for:
- General crypto trading advice
- Other exchanges (Binance, OKX direct trading)
- Non-hedging strategies

## Prerequisites

### Platforms

- [PaperTrade](https://papertrade.xyz/) — Perps exchange on Hyperliquid, loss = mint PAPER
- [ONDO](https://app.ondoperps.xyz/?ref=8RU3VB) — Perps exchange for the hedge leg

### Getting API Keys

1. **PaperTrade**: Import or create a HyperEVM wallet. The wallet private key is used directly.
2. **ONDO API Key**: Create at [ONDO App](https://app.ondoperps.xyz/?ref=8RU3VB) → Settings → API Keys

### For New Users

- **Crypto**: [OKX](https://www.mitxcqvwnhj.com/join/9122359) | [Binance](https://www.bsmkweb.cc/register?ref=35266688)
- **Automation**: [Minara](https://minara.ai/r/23EUC6)
- **AI local**: [GPT](https://www.gamsgo.com/partner/JwUY7)

### Dependencies

```bash
pip install -r requirements.txt
```

## Instructions

### Project Path

`/Users/caroline/Desktop/源代码/demo/paper中性脚本/`

### Method 1: Web Control Panel (Recommended)

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本
python web_server.py
```

Open **http://localhost:8765/** in browser.

Panel features:
- 🧪 Mock / 💰 Real mode switch (default: mock)
- 🌐 Chinese / English language switch
- ▶ Start / ■ Stop bot
- 📊 Real-time runtime logs (refresh every 3s)

### Method 2: Command Line

#### 1. Configure `.env`

```bash
cp .env.example .env
```

Edit `.env`:

```ini
# Run mode: mock (no real trades) or real
HEDGE_MODE=mock

# PaperTrade wallet private key (0x-prefixed 64-char hex)
PAPER_WALLET_PRIVATE_KEY=0x...

# PaperTrade Session Key (optional, auto-registered if empty)
PAPER_SESSION_KEY=

# ONDO API credentials
ONDO_KEY_ID=ondoKeyId_xxx
ONDO_API_SECRET=ondoApiSecret_xxx

# Strategy parameters
HEDGE_SYMBOL=BTC
HEDGE_POSITION_SIZE=50
HEDGE_PAPER_LEVERAGE=10
HEDGE_ONDO_LEVERAGE=10
HEDGE_TARGET_MOVE_PCT=1.0
HEDGE_MAX_HOLD_SECONDS=3600
HEDGE_POLL_INTERVAL=10
HEDGE_MAX_CYCLES=200
HEDGE_DIRECTION=random
```

#### 2. Register Session Key (Real mode only)

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本
python main.py register
```

Copy the output `PAPER_SESSION_KEY` into `.env`.

#### 3. Check Account Status

```bash
python main.py status
```

#### 4. Run the Bot

```bash
python main.py
```

#### 5. Emergency Close All

```bash
python main.py close-all
```

## Mode Explanation

| Mode | `HEDGE_MODE` | Behavior |
|------|--------------|----------|
| Mock | `mock` | Uses built-in mock clients, no real trades, no credentials needed |
| Real | `real` | Real trading, requires wallet key and ONDO API credentials |

Mock mode uses a fixed test wallet and outputs identical log format to real mode. Good for demos and learning.

## Strategy Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `HEDGE_SYMBOL` | BTC | Trading pair (BTC/ETH) |
| `HEDGE_POSITION_SIZE` | 50 | Notional position size per side (USD) |
| `HEDGE_PAPER_LEVERAGE` | 10 | PaperTrade leverage |
| `HEDGE_ONDO_LEVERAGE` | 10 | ONDO leverage (BTC/ETH max 25) |
| `HEDGE_TARGET_MOVE_PCT` | 1.0 | Price move % to trigger close |
| `HEDGE_MAX_HOLD_SECONDS` | 3600 | Max hold time before forced close |
| `HEDGE_DIRECTION` | random | Direction: random / paper_long / paper_short |

## Strategy Logic

1. Open opposite positions on PaperTrade and ONDO simultaneously
2. PaperTrade side always loses → mints PAPER tokens (~95 PAPER/$1 loss)
3. ONDO side always wins → earns points + USDC
4. Net PnL ≈ 0 (minus ONDO fees ~0.05% round-trip)
5. Profit = PAPER tokens + ONDO points

## Examples

### Example 1: Quick mock mode demo

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本
HEDGE_MODE=mock HEDGE_MAX_CYCLES=1 HEDGE_MAX_HOLD_SECONDS=10 python main.py
```

### Example 2: Start web panel and run via browser

```bash
python web_server.py
# Open http://localhost:8765, click "Start Bot"
```

### Example 3: Real mode with BTC, $100 position, 10x leverage

```ini
HEDGE_MODE=real
HEDGE_SYMBOL=BTC
HEDGE_POSITION_SIZE=100
HEDGE_PAPER_LEVERAGE=10
HEDGE_ONDO_LEVERAGE=10
```

```bash
python main.py
```

## Error Handling

### Session Key Expired
```
RuntimeError: Session Key 已过期，请重新注册
```
Run `python main.py register` to re-register.

### ONDO Signature Error
```
ONDO API 错误: signature invalid
```
Verify `ONDO_KEY_ID` and `ONDO_API_SECRET`. If still failing, the ONDO API signature format may have changed — update `_sign` method in `ondo_client.py`.

### PaperTrade Close Position Not Found
Open intents have on-chain confirmation delay. The bot has a built-in 60s wait. If timeout, retry with `python main.py close-all`.

### Insufficient Balance
Ensure both PaperTrade wallet and ONDO account have enough USDC. PaperTrade needs at least `HEDGE_POSITION_SIZE / HEDGE_PAPER_LEVERAGE * 1.5` USDC.

### Web Panel Logs Empty
Ensure started via `python web_server.py`. The service uses `-u` unbuffered output; logs write to `bot.log` in real-time.

## Verification

```bash
cd /Users/caroline/Desktop/源代码/demo/paper中性脚本

# Module import
python -c "import paper_client, ondo_client, hedge_bot, mock_clients, main; print('OK')"

# Mock mode full flow
HEDGE_MODE=mock HEDGE_MAX_CYCLES=1 HEDGE_MAX_HOLD_SECONDS=10 python main.py

# ONDO public API
python -c "
from ondo_client import OndoClient, OndoConfig
c = OndoClient(OndoConfig(key_id='t', api_secret='t'))
print('BTC:', c.get_mark_price('BTC-USD.P'))
"
```

## Security

- This skill only makes outbound requests to `exchange.papertrade.xyz` and `api.ondoperps.xyz`.
- It does not read local files outside the project directory, store credentials, or make requests to any other domains.
- Session Key can only trade, **cannot withdraw** — even if leaked, funds are safe.
- Web service binds to `127.0.0.1` only, not exposed externally.
- Mock mode is the default to prevent accidental real trades.
- No hardcoded credentials in source code.
- Source code is publicly available at https://github.com/0xcii/paper-ondo-hedge-bot

## Core Files

| File | Purpose |
|------|---------|
| `paper_client.py` | PaperTrade client (EIP-712 signing, Session Key, open/close) |
| `ondo_client.py` | ONDO Perps client (HMAC signing, market orders, queries) |
| `mock_clients.py` | Mock clients for demo mode |
| `hedge_bot.py` | Core hedge logic (dual open, monitor, close, stats) |
| `main.py` | CLI entry point |
| `web_server.py` | Web control panel backend (port 8765) |
| `index.html` | Web control panel frontend |
| `.env.example` | Config template |
