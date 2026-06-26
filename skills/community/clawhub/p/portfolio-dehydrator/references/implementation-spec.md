# Implementation Spec

Use this file when the request asks for exact Portfolio Master behavior or when a PRD must be translated into code with low ambiguity.

## Input Contract

- Main callable should accept `tokens: list[str]` and `total_capital: float = 10000`.
- Also support an optional original-allocation input such as `current_weights`, and use it for the "before vs after" comparison whenever the user supplied it.
- If the user provides comma-separated text instead of a list, add a lightweight normalization helper before calling the core optimizer.
- The backend should directly accept these entry styles:
  - Natural-language text such as "我现在 40% BTC、30% ETH、30% USDT"
  - Ticker list
  - Explicit weight text such as `BTC=40,ETH=30,USDT=30`
- Screenshot OCR and wallet/address ingestion may exist in the surrounding product, but they should be normalized upstream into token symbols plus optional weights before calling this backend.
- If the surrounding product supports Ethereum, BNB Chain, Arbitrum, Base, Optimism, Polygon, Avalanche, Solana, or Tron, convert chain balances into token symbols in the input layer before invoking the optimizer.
- Preserve partial execution: one bad ticker must not invalidate the full request.

## Data Contract

- Use the past 30 days of 4-hour candles.
- Target candle count is 180. Treat fewer than 84 candles as insufficient-history new tokens.
- Prefer OKX hosts that are more resilient for mainland-China connectivity:
  - `https://aws.okx.com`
  - `https://www.okx.com`
- After two consecutive OKX failures for the same asset, fall back in order to:
  - `Gate.io`
  - `Bybit`
  - `Bitget`
- Handle rate limits, timeouts, and malformed responses with retries and bounded backoff.
- Do not use synthetic mock price paths in production mode. When both APIs fail, skip the affected asset, keep partial execution when possible, and fall back to a cash-only recommendation if no real-data portfolio can be built.
- For invalid tickers, use fuzzy suggestions when practical and otherwise return a graceful warning while continuing with valid assets.
- Use sample-tiering instead of a single hard cut:
  - fewer than `12` candles: skip the asset
  - `12-35` candles: keep it in the report and model as a low-confidence short sample
  - `36-83` candles: keep it as a usable but still incomplete sample
  - `84+` candles: treat as a standard sample

## Quant Contract

- Build aligned close-price time series before computing returns, covariance, and correlation.
- Use `PERIODS_PER_YEAR = 6 * 365` for 4-hour data.
- Annualize volatility with `std(periodic_returns) * sqrt(PERIODS_PER_YEAR)`.
- Annualized expected return can use a compounded interpretation from mean 4-hour return or cumulative growth, but the choice must be internally consistent and explained in code comments.
- Use Sortino to measure downside-adjusted efficiency, Calmar to relate return to max drawdown, and max drawdown itself to quantify the downside floor.
- Stablecoins serve as the risk-free reference and should not distort the risky-asset covariance matrix.
- Mark correlation `>= 0.85` as overlap risk.
- Penalize lower-quality assets inside overlap groups through bounds, objective penalties, or post-processing that clearly biases allocation toward the better Sortino / Calmar / max-drawdown profile.
- Assets with weak recent-sample Sortino / Calmar or overly deep max drawdown may receive a stricter effective cap than their public category hard cap, allowing extra cash buffer instead of forcing low-quality risk exposure.
- Optimize with `scipy.optimize.minimize(..., method="SLSQP")`.
- Enforce:
  - Sum of weights equals `1.0`
  - `BTC` and `ETH` cap at `0.50`
  - Configured blue-chip tokens cap at `0.30`
  - Unlisted long-tail or meme tokens cap at `0.15`
  - New tokens cap at `0.05`
- If optimization fails, fall back to a deterministic capped allocation that still respects weights and favors better downside-adjusted assets.

## Report Contract

Output must be a professional Chinese Markdown report with these sections:

- Use a dual-layer writing style:
  - Layer 1: give the direct recommendation fast for business users.
  - Layer 2: explain the quant reason in plain Chinese so non-expert clients can still follow the logic.
- Prefer customer-ready wording over purely internal analyst shorthand.
- Avoid repeating the same conclusion across adjacent sections; each section should contribute a distinct layer of evidence.
- Add a source-transparency layer showing data source, candle count, sample band, and data-confidence label for each asset.
- Add a simple scenario stress test so the report explains how the optimized portfolio behaves under a few downside environments.

Recommended opening block before the numbered sections:

- `执行摘要`
- Summarize the main portfolio problem, the main keep/add/reduce calls, and whether the optimized mix is offensive, balanced, or defensive.

1. `风险重叠警告`
- List correlation-overlap pairs above `0.85`.
- Explain which asset should be reduced or removed based on Sortino / Calmar / max-drawdown comparison.
- If no overlaps exist, explicitly state that the structure looks healthy.

2. `资产效率分析`
- Identify the strongest asset by downside-adjusted efficiency and drawdown quality.
- Identify the weakest asset by poor downside-adjusted efficiency or overly deep drawdown.
- Call out `[高风险盲盒]` assets separately when present.

3. `最终优化比例建议`
- Show each token's optimized percentage.
- Show the corresponding `USDT` amount based on `total_capital`.
- Make the list directly actionable.
- Add role/action hints such as core position, satellite position, observation position, or cash buffer.
- Separate true high-conviction positions from low-confidence or constraint-driven placeholder holdings.
- Add a short rebalancing sequence for customers who want to implement the change step by step.
- Include a dedicated "before vs after" weight table using user-supplied original weights when available; only use equal-weight when no user allocation was provided.

4. `💡 优化效果`
- Summarize expected volatility reduction, max-drawdown improvement, and Sortino / Calmar improvement versus the active reference portfolio in one sentence.

Recommended closing block after the numbered sections:

- `指标说明`
- Briefly explain correlation, volatility, Sortino, Calmar, and max drawdown in plain Chinese without assuming quant background.

## Code Delivery Contract

- Deliver one tidy Python file.
- Include all required imports.
- Use detailed Chinese comments and type hints.
- End with a standalone `requirements.txt` block containing:
  - `requests`
  - `pandas`
  - `numpy`
  - `scipy`
