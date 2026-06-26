# Polymarket Arb Scanner Pro

Pure math arbitrage on Polymarket. Finds markets where YES + NO < $0.94 (6¢+ gap). No prediction required — guaranteed profit at resolution. Includes liquidity filter, market blacklist, and SQS integration for automated execution.

## What It Does

- Scans up to 500 Polymarket markets sorted by 24h volume
- Finds YES + NO sum < $1.00 — pure arbitrage with locked-in profit
- Default minimum edge: 2¢ (covers gas + slippage)
- Executes both legs as Fill-or-Kill (FOK) — no leg risk
- Risk manager integration (position limits, rate limiting)
- Kelly-like sizing within deployable balance

## The Math

If YES costs 45¢ and NO costs 50¢ = total 95¢ to hold both.
At resolution, one pays $1.00. Locked-in profit: 5¢ on 95¢ deployed = **5.3% risk-free return**.

```
edge = 1.00 - (yes_price + no_price)
profit = edge * deploy_size
```

## Setup

```bash
pip install requests
```

Configure `.env` in script directory:
```
PRIVATE_KEY=your_polygon_private_key  
WALLET_ADDRESS=0xYourPolymarketWallet
```

Or export as environment variables.

## Usage

```bash
# Scan only (dry run)
python3 arb_scanner.py

# Set minimum edge
python3 arb_scanner.py --min-edge 0.04

# Scan more markets
python3 arb_scanner.py --limit 1000

# Execute found arbs
python3 arb_scanner.py --buy

# Execute with custom deployment size
python3 arb_scanner.py --buy --max-deploy 100
```

## Execution

- Both legs execute as FOK simultaneously
- If either leg fails → no position taken (safe)
- Maximum 3 arbs executed per run
- Keeps $10 reserve in wallet at all times

## Risk Management

Integrates with `risk_manager.py` if present:
- Per-market position limits
- Rate limiting (no order spam)
- Portfolio exposure tracking

## Output Example

```
⚡  POLYMARKET ARB SCANNER
    Min edge: 2.0% | Scanning 500 markets

📡 Fetching markets...
   483 markets loaded

⚡ Found 3 arb opportunity(ies):

  Edge    YES      NO    Vol24h  Question
  ----   ---      --    ------  --------
  4.2%  48.0%  47.8%  $892,341  Will Bitcoin exceed $100k by March?
  3.1%  31.0%  65.9%   $45,201  Will Fed cut rates in March 2025?
  2.3%  72.1%  25.6%  $234,882  Will the Lakers win the championship?
```

## Requirements

- Python 3.9+
- `py_clob_client`: `pip install polymarket-clob-client`
- Polymarket wallet with USDC on Polygon

## Notes

Pure arb opportunities are rare (market is fairly efficient). This scanner checks the top volume markets where pricing inefficiencies are most likely due to high trading activity and bid-ask spread dynamics.
