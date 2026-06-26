# Maxxit 0G Skill

Use Maxxit Lazy Trading with 0G decentralized compute for portfolio-aware trade decisions and 0G decentralized storage for verifiable alpha listings.

## Installation

### Via ClawHub CLI
```bash
npx clawhub@latest install maxxit-0g
```

### Manual Installation
Copy the `maxxit-0g` folder to:
- Global: `~/.openclaw/skills/`
- Workspace: `<project>/skills/`

## Configuration

Set these environment variables:

```bash
export MAXXIT_API_KEY="lt_your_api_key_here"
export MAXXIT_API_URL="https://maxxit.ai"
```

## Quick Start

1. **Get an API Key**: 
   - Visit [maxxit.ai/lazy-trading](https://maxxit.ai/lazy-trading)
   - Connect your wallet
   - Complete the setup wizard
   - Generate an API key from your [dashboard](https://www.maxxit.ai/dashboard)

2. **Configure**: Set environment variables

3. **Use**: Ask your assistant to send trading signals!

## Example Usage

```
"Should I trade BTC?"

"What does 0G think about ETH?"

"Make a portfolio-aware AI decision for SOL"

"Send a trading signal: Long ETH 5x leverage at 3200"

"Check my lazy trading account status"

"Execute a short on BTC with 10x leverage, TP 60000, SL 68000"

"List this trade as alpha on 0G storage"
```

## 0G Features

- **0G Compute Decision Workflow**: The skill can call Maxxit's `/alpha/0g-decision` endpoint with your deployment context and market research summary, then present `shouldTrade`, `side`, `confidence`, and `reasoning`.
- **Sponsored Inference**: 0G decisions are sponsored by the platform and do not deduct user LLM credits.
- **0G Storage for Alpha**: When a verified trade is listed as alpha, Maxxit uploads the alpha content to 0G storage when available and returns a `rootHash` for independent buyer verification.

## Supported Venues

- **Ostium** - Perpetual futures on Arbitrum
- **Aster DEX** - Perpetual futures on BNB Chain (testnet setup in Maxxit)
- **Avantis DEX** - Perpetual futures on Base mainnet
- **Alpha Marketplace** - Trustless ZK-verified trading signals with optional 0G storage proofs

## Built-in Strategy Scripts

The skill includes standalone Python strategy scripts. Use them when the user wants the agent to run a predefined trading system.

- `ema-strategy.py` - EMA crossover trend-following strategy
- `rsi-bollinger-strategy.py` - RSI + Bollinger Band mean reversion strategy
- `donchian-adx-strategy.py` - Donchian breakout with ADX trend filter
- `taker-strategy.py` - Aggressive Taker (Order Flow) HFT strategy. Analyzes Binance taker buy/sell ratios to detect aggressive market participants and catch rapid momentum shifts.
- `mean-reversion-strategy.py` - RSI + Bollinger Band mean-reversion strategy. A technical approach using price exhaustion points optimized for high-frequency scalping in sideways or boring markets.
- `breakout-strategy.py` - Volatility breakout strategy with ATR filter. Enters trades when price breaks out of a standard deviation channel while ATR confirms increasing volatility and momentum.
- `vwap-strategy.py` - VWAP crossover institutional momentum strategy. Uses volume-weighted average price and EMA to confirm institutional trend alignment and confirm trade strength with volume.

Each script fetches Binance klines, derives signals locally, and routes execution through the Maxxit Lazy Trading API.

### Command Line Usage
All scripts support dynamic `--symbol` (e.g. `BTC/USD`) and `--venue` (`OSTIUM` or `AVANTIS`) arguments.

```bash
python taker-strategy.py --symbol BTC/USD --venue AVANTIS
python vwap-strategy.py --symbol ETH/USD --venue OSTIUM
```

## Links

- [Maxxit App](https://maxxit.ai)
- [Lazy Trading Setup](https://maxxit.ai/lazy-trading)
- [0G](https://0g.ai)
- [GitHub](https://github.com/Maxxit-ai/maxxit-latest)
