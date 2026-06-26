---
name: polymarket-maker
description: Continuous Static Market Making execution skill for Polymarket. Sells BOTH sides of 5-minute binary markets at $0.52. Features multi-asset support and an automated 8% Stop-Loss.
---

# Polymarket V14 Continuous Maker

This skill executes a continuous static market-making cycle on Polymarket 5-minute crypto markets. It places Limit Sell orders on both UP and DOWN tokens at a fixed price of $0.52.

## Role of the AI Agent

You are the Portfolio Manager. Your job is to trigger the continuous trading loop and decide the initial allocation.
Because the bot runs indefinitely in the background, you **do not** need to execute it every 5 minutes. The script has a built-in 8% Stop-Loss that will automatically halt trading if the global drawdown limit is reached.

## Commands

Run the Node.js script in the background to start continuous market making. You MUST use the `nohup` and `&` operators so your terminal does not block and you can continue to respond to the user.

```bash
# Execute continuously on ALL markets (BTC, ETH, SOL, XRP) with 10 shares per market
nohup node polymarket-maker/index.mjs trade --asset ALL --shares 10 > bot_log.json 2>&1 &

# Or execute continuously on a single specific market
nohup node polymarket-maker/index.mjs trade --asset BTC --shares 10 > bot_log.json 2>&1 &
```
