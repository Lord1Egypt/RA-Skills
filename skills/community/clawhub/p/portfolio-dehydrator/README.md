# Portfolio Dehydrator

In Web3, risk does not become diversified simply because a portfolio holds more tokens. More often, it becomes harder to see. `Portfolio Dehydrator` is a quantitative portfolio diagnosis and allocation optimization skill for Web3 investors. It exposes redundant overlap, measures downside-adjusted quality, and rebuilds a cleaner, more defensible allocation structure through evidence-based risk controls.

## What It Does

- Detects portfolio exposures that look diversified on the surface but are still highly overlapping underneath
- Uses `Sortino`, `Calmar`, `maximum drawdown`, and correlation instead of relying on simple price performance
- Produces executable allocation recommendations and client-facing reports under strict position constraints
- Handles unstable access conditions with a real-data-only fallback chain: `OKX` first, then `Gate.io`, `Bybit`, and `Bitget`
- Preserves valid real analysis where possible and skips assets with insufficient data instead of inventing mock prices
- Explains result reliability through sample-tier labels and data-confidence grading
- Adds a lightweight portfolio stress test so clients can understand likely loss boundaries under common downside scenarios

## Why It Is Different

Most Web3 portfolio tools focus on profit and loss tracking. This skill focuses on three harder and more important questions:

1. Is the portfolio genuinely diversified, or only pretending to be?
2. Is the volatility being taken actually worth it?
3. Which positions deserve capital, and which ones should yield to higher-quality assets or cash buffers?

It is not a tool for predicting the next explosive token. It is a portfolio decision framework centered on risk-adjusted efficiency.

## Decision Framework

The underlying logic is grounded in Modern Portfolio Theory and adapted for the realities of Web3 portfolio construction:

- `Correlation matrix`: identifies highly overlapping asset pairs and helps avoid false diversification
- `Sortino ratio`: measures return efficiency after penalizing downside volatility
- `Calmar ratio`: compares return to maximum drawdown
- `Maximum drawdown`: directly measures the downside floor for a portfolio or single asset
- `Constrained optimization`: uses `scipy.optimize` with `SLSQP` to allocate weights under strict caps

The current public constraints include:

- `BTC` and `ETH`: hard cap `50%` per asset
- Blue-chip majors: hard cap `30%` per asset
- Long-tail / meme assets: hard cap `15%` per asset
- Newly listed assets with insufficient data: hard cap `5%` per asset

If an asset shows any of the following characteristics in the recent sample:

- weak downside-adjusted quality
- excessively deep maximum drawdown
- strong overlap with a superior asset

the system further tightens its effective cap and prefers to allocate that capital to stronger assets or a `USDT` cash buffer.

## Inputs

The current backend supports the following input forms:

- Token list: `BTC ETH SOL PEPE`
- Natural-language holdings text: `I currently hold 40% BTC, 30% ETH, 20% PEPE, and 10% USDT`
- Structured parameters:
  - `tokens: list[str]`
  - `total_capital: float`
  - `current_weights: dict[str, float]`

Notes:

- If the user provides starting weights, the report compares the optimized portfolio against the real current allocation
- If starting weights are not provided, the system falls back to an equal-weight risky-asset reference portfolio
- Screenshot OCR, wallet parsing, and on-chain balance aggregation should be handled upstream before normalized token symbols and weights are passed into this backend

## Outputs

The output is a client-facing Chinese Markdown report that typically includes:

- Executive summary
- Pairwise asset correlation table
- Single-asset profile table
- Risk overlap conclusions
- Before-vs-after portfolio comparison
- Final recommended allocation
- Rebalancing sequence
- Compliance and risk disclosure

## Example Use Cases

- "Check whether `BTC ETH SOL PEPE ARB` has hidden overlap."
- "I currently hold `35% BTC, 25% ETH, 20% LINK, 10% ARB, and 10% USDT`. How should I optimize it?"
- "Generate a more professional client-facing portfolio diagnosis report, not just a final weight table."

## Repository Structure

```text
web3-portfolio-optimizer/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── requirements.txt
│   └── web3_portfolio_optimizer.py
└── references/
    └── implementation-spec.md
```

## Quick Start

### 1. Install dependencies

```bash
python3 -m pip install -r assets/requirements.txt
```

### 2. Run the bundled backend

```bash
python3 assets/web3_portfolio_optimizer.py --tokens BTC,ETH,PEPE,ARB --capital 10000
```

### 3. Run with current holdings

```bash
python3 assets/web3_portfolio_optimizer.py \
  --tokens BTC,ETH,USDT,PEPE \
  --capital 10000 \
  --weights "BTC=40,ETH=30,USDT=20,PEPE=10"
```

## Validation

This skill currently passes local structural validation:

```bash
python3 /Users/shaozhaoru/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## Security Notes

- The current implementation only calls public market-data endpoints and does not require wallet private keys
- Stablecoins are treated as the risk-free benchmark and cash buffer
- Historical analysis is not a promise of future returns
- Client-facing deployments should disclose that past performance does not guarantee future results

## Publishing Notes

- GitHub Repository: <https://github.com/Shaozrrr/portfolio-dehydrator-skill>
- Public name: `Portfolio Dehydrator`
- Skill trigger name: `web3-portfolio-optimizer`

## License

MIT
