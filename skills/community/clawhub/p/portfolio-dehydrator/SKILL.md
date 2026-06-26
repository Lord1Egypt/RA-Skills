---
name: web3-portfolio-optimizer
description: Portfolio Dehydrator is a Web3 portfolio diagnosis and allocation optimization skill. Use it when the user wants Codex to turn a PRD or coding request into a backend or skill script that fetches crypto OHLCV data from OKX with Gate.io, Bybit, and Bitget fallback, diagnoses hidden overlap, compares Sortino, Calmar, and maximum drawdown, performs constrained SLSQP weight optimization, and emits a polished Chinese Markdown report with source transparency, data-confidence grading, and real-data-only degradation.
license: MIT
metadata:
  version: 1.0.3
  author: Shaozhaoru
  requires:
    - python3
    - requests
    - pandas
    - numpy
    - scipy
  repository: https://github.com/Shaozrrr/portfolio-dehydrator-skill
  install:
    type: python
    command: python3 -m pip install -r assets/requirements.txt
  env: []
---

# Portfolio Dehydrator

In Web3, risk does not disappear simply because a portfolio holds more assets; more often, it accumulates in subtler forms beneath the surface. `Portfolio Dehydrator` is built on the discipline of Modern Portfolio Theory, combining asset correlation, Sortino, Calmar, maximum drawdown, and strict allocation constraints to deconstruct and rebuild portfolio structure with precision. It identifies redundant exposure, measures downside-adjusted efficiency, compresses unproductive volatility, and reallocates capital toward positions more worthy of the risk they demand. What it delivers is not a superficial rebalance suggestion, but an evidence-based portfolio judgment rooted in risk-return efficiency, turning a crowded portfolio into a coherent one.

Implement a single-file Python backend for this skill. Produce executable code first, keep prose minimal, and default to Chinese comments and report text unless the user asks otherwise.

## Workflow

1. Convert the request into code, not a long explanation.
- Build one clean Python file with all imports, helpers, domain models, optimizer logic, and a callable entry point.
- If the user explicitly asks for "code only", return only code plus a separate `requirements.txt` block.

2. Load the exact delivery contract when needed.
- Read [references/implementation-spec.md](references/implementation-spec.md) whenever the request includes detailed product requirements, optimization constraints, error-handling rules, or report-format requirements.
- Reuse [assets/web3_portfolio_optimizer.py](assets/web3_portfolio_optimizer.py) as the starting template when the user wants a full backend file quickly; adapt parameters, token white lists, and report wording instead of rewriting from scratch.

3. Implement the four required modules.
- Input module: accept `tokens: list[str]` and `total_capital: float = 10000`.
- If the user provides current allocation ratios, use them as the original portfolio baseline; only fall back to equal-weight comparison when no starting weights are supplied.
- Data module: use OKX first, then degrade to Gate.io, Bybit, and Bitget, skip K-line fetch for stablecoins, support retries, timeouts, fuzzy ticker handling, and fail closed without synthetic mock pricing.
- Quant module: compute 4h return series, annualized return and volatility, correlation matrix, Sortino, Calmar, max drawdown, overlap penalties, and SLSQP optimization with hard caps.
- Output module: return polished Chinese Markdown with risk overlap warnings, asset efficiency analysis, source-transparency tables, stress testing, optimized allocation, and one-line optimization impact.

4. Preserve production behavior.
- Use `requests`, `pandas`, `numpy`, and `scipy.optimize`.
- Add detailed Chinese comments and type hints.
- Keep data acquisition and optimization logic decoupled so future wallet or on-chain inputs can be added without rewriting core math.
- The current backend accepts normalized token lists plus optional holdings text / parsed `current_weights`; screenshot OCR, wallet-address resolution, and chain-balance aggregation should be handled by the surrounding product before invoking this backend.

## Implementation Rules

- Normalize token symbols to uppercase and map common spot symbols to `-USDT` or `_USDT` formats as required by the exchange.
- Treat `USDT`, `USDC`, and `DAI` as stablecoins excluded from the risky-asset covariance matrix, and use `R_f = 0.04`.
- Treat assets with fewer than 84 four-hour candles as `[High-Risk Blind Box]` and cap them at `0.05`.
- Mark any pair with Pearson correlation `>= 0.85` as `[Risk Overlap Group]`.
- Within each overlap group, penalize or effectively suppress the lower-quality asset based on Sortino, Calmar, and max drawdown instead of letting both assets receive full unconstrained weights.
- If an asset shows weak downside-adjusted quality or overly deep drawdown in the recent sample, tighten its effective optimization cap below the public hard cap and prefer cash over forcing that asset into a large weight.
- Use deterministic cap buckets: `BTC` and `ETH` at `0.50`, configured blue-chip whitelist at `0.30`, default long-tail assets at `0.15`, new tokens at `0.05`.
- Make caps and token-category lists explicit and easy to edit near the top of the file.

## Output Rules

- Emit professional Chinese Markdown.
- Default to a client-facing report style: professional but readable for non-quant users.
- Support product-style input guidance before analysis: the backend directly supports ticker lists and natural-language holdings text such as `I currently hold 40% BTC, 30% ETH, and 30% USDT`.
- Treat current weights provided by the user as authoritative for "before vs after" comparison; do not overwrite them with an equal-weight assumption.
- If no current weights are provided, explicitly state that the report uses equal-weight as the default reference portfolio.
- Add source transparency and data-confidence grading so the reader can see which exchange supplied each asset, how many candles were available, and whether the sample should be treated as high, medium, or low confidence.
- If the surrounding product accepts screenshots or wallet / address input from Ethereum, BNB Chain, Arbitrum, Base, Optimism, Polygon, Avalanche, Solana, or Tron, convert those holdings into token symbols before calling this backend.
- Include concrete percentages and `USDT` amounts based on `total_capital`.
- Add an executive summary, plain-language explanations, and actionable rebalancing guidance instead of only listing raw metrics.
- Keep technical indicators, but immediately explain what they mean in everyday language when the audience is not explicitly technical.
- Compare the optimized portfolio against the active reference portfolio: use the user-supplied starting allocation when available, otherwise fall back to equal-weight.
- Distinguish high-conviction adds from low-confidence or constraint-driven holdings so customer-facing wording stays aligned with the actual quantitative scores.
- Never crash on bad tickers, rate limits, or full API outage. Degrade gracefully by skipping unavailable assets or returning a cash-only recommendation; do not invent synthetic price paths.
- When the user requests deliverable code, do not add explanatory prose outside the requested code blocks.

## Resources

### references/
- [references/implementation-spec.md](references/implementation-spec.md): PRD-derived contract covering data windows, annualization, fallback behavior, optimization constraints, and report structure.

### assets/
- [assets/web3_portfolio_optimizer.py](assets/web3_portfolio_optimizer.py): bundled single-file Python implementation with OKX/Gate.io fallback, real-data-only degradation, SLSQP optimization, and Chinese Markdown reporting.
- [assets/requirements.txt](assets/requirements.txt): minimal dependency list for the bundled Python implementation.

## Security Notes

- External requests are limited to public market-data endpoints on `OKX`, `Gate.io`, `Bybit`, and `Bitget`.
- The bundled backend does not persist portfolio data to disk.
- No API key or wallet private key is required by the current implementation.
- If an upstream product accepts screenshots or wallet addresses, preprocess them locally and pass only normalized token symbols and optional weights into this backend.

---

**Maintainer**: Shaozhaoru  
**License**: MIT
