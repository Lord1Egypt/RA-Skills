---
name: polymarket-bundle-crypto-fade-trader
description: Fades strong directional crypto moves on Polymarket 5-minute interval markets. After 3+ consecutive high-conviction same-direction intervals (>58% probability), the next interval tends to mean-revert -- a well-documented microstructure effect in crypto. Targets BTC, ETH, and SOL Up or Down bundles with conviction-based position sizing scaled by streak strength.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Bundle Crypto Momentum Fade Trader
  difficulty: advanced
---

# Bundle -- Crypto Momentum Fade Trader

> **This is a template.**
> The default signal detects strong directional streaks in crypto 5-minute interval markets and fades them using conviction-based sizing. The skill handles all the plumbing (interval parsing, streak detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists 5-minute interval markets for BTC, ETH, and SOL: "Will BTC be Up or Down in the 14:00-14:05 ET interval?" These resolve to YES (up) or NO (down) based on the actual price movement. When a coin moves sharply in one direction over 15-30 minutes -- 3 to 6 consecutive strong same-direction intervals at >58% probability -- the NEXT interval tends to mean-revert. This is the "momentum fade," a well-documented microstructure effect in crypto markets where short-term directional momentum exhausts itself and reverses.

## Edge

Unlike a generic streak trader that counts any streak of >50% intervals, this skill specifically targets **strong** directional moves where each interval in the streak exceeds the FADE_THRESHOLD (default 58%). This filters out noise and focuses on genuine momentum exhaustion events. The fade is structurally sound because:

1. **Microstructure mean-reversion** -- short-horizon crypto returns exhibit negative autocorrelation after extended directional moves, documented across BTC, ETH, and SOL on 5-minute timeframes
2. **Retail momentum chasing** -- Polymarket participants observe a streak and price the next interval as a continuation, creating a systematic overpricing of momentum
3. **Arbitrage-free pricing constraint** -- the 5-minute return distribution has bounded variance; after 3+ consecutive strong-direction intervals, the conditional probability of continuation drops below the unconditional probability
4. **Bundle structure** -- each interval resolves independently, so a streak of 3 strong-up intervals does not mechanically cause the 4th to also be up

## Signal Logic

1. Discover crypto interval markets via keyword search (`Bitcoin Up or Down`, `BTC Up or Down`, `Ethereum Up or Down`, `Solana Up or Down`) with a `get_markets(limit=200)` fallback
2. Parse each question to extract (coin, date, start_time, end_time) using regex
3. Group intervals by (coin, date) and sort by time
4. Scan each group for streaks of `FADE_LENGTH`+ consecutive intervals where ALL have probability >= `FADE_THRESHOLD` (strong-up) or <= `1 - FADE_THRESHOLD` (strong-down)
5. After detecting a strong move, check the NEXT interval:
   - **Strong-up streak** -> next interval should mean-revert down; if still priced >= `NO_THRESHOLD`, sell NO
   - **Strong-down streak** -> next interval should mean-revert up; if still priced <= `YES_THRESHOLD`, buy YES
6. Size by conviction (distance from threshold), not flat amount

### Remix Signal Ideas

- **Binance/Coinbase websocket** -- feed real-time order flow data to detect momentum exhaustion before the 5-minute interval resolves; trade the interval market while the fade is still mispriced
- **Funding rate signal** -- when perpetual funding rates are extremely positive/negative, the fade has higher expected value because leveraged positions are being unwound
- **Volume profile** -- weight the streak detection by actual trading volume in each interval; high-volume directional moves exhaust faster than low-volume drifts
- **Cross-coin correlation** -- if BTC has a strong-up streak and ETH/SOL have not yet followed, the fade on BTC is weaker (genuine broad move) vs. BTC-only streaks (more likely noise)
- **Volatility regime** -- adjust FADE_THRESHOLD dynamically based on realised volatility; in high-vol regimes, require stronger streaks before fading

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` mean nothing runs automatically until configured in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade at full conviction |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `1` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this |
| `SIMMER_FADE_THRESHOLD` | `0.58` | Min probability for a "strong" interval in streak detection |
| `SIMMER_FADE_LENGTH` | `3` | Min consecutive strong intervals to trigger a fade |

## Edge Thesis

Crypto 5-minute interval markets on Polymarket exhibit momentum chasing by retail participants. When a coin moves sharply in one direction -- 3+ consecutive intervals where each is priced at >58% in the same direction -- the pricing of the next interval systematically overestimates continuation probability. This is a direct consequence of short-horizon mean-reversion in crypto microstructure: after extended directional moves, the conditional probability of further continuation drops below the market-implied probability. The fade exploits this gap with conviction-based sizing that scales with the distance from the trading threshold.

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
