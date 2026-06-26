# Adapter: Quantitative Finance

Use this adapter when the paper addresses asset pricing, derivative pricing, hedging, forecasting, execution, portfolio choice, market microstructure, or another finance problem where stochastic modeling and market frictions matter.

## What to prioritize

1. The task: pricing, hedging, forecasting, execution, or allocation.
2. State variables, stochastic dynamics, and information structure.
3. Measure choice, no-arbitrage logic, martingale structure, or utility criterion when relevant.
4. Calibration or estimation procedure.
5. Backtest design and evaluation metrics.
6. Frictions: transaction costs, turnover, liquidity, slippage, constraints, and financing assumptions.

## Questions to answer in the note

- What finance problem is being solved exactly?
- What stochastic assumptions or market structure assumptions matter most?
- Is the paper deriving a pricing relation, estimating a predictive signal, or optimizing a decision rule?
- How is the model calibrated or trained?
- Are the results out-of-sample and risk-adjusted?
- Would the reported edge survive realistic trading frictions?

## Minimum insertions into the note

Add or expand these sections:

### Problem setup

- market setting and asset universe
- objective and decision variable
- stochastic process or state evolution
- information set and constraints

### Technical core

- governing pricing / forecasting / control equation
- calibration or estimation procedure
- risk measure or utility criterion
- assumptions behind no-arbitrage or decision optimality if relevant

### Evidence

- backtest split and protocol
- evaluation metrics
- turnover and cost accounting
- drawdown, tail risk, or risk-adjusted results

### Limitations and failure modes

Include at least one discussion of:

- look-ahead bias
- leakage or survivorship bias
- overfitting to one market regime
- unrealistic execution assumptions
- weak out-of-sample evidence

## Special reading rules

- Distinguish carefully between pricing theory, statistical prediction, and implementable trading performance.
- Ask whether the edge is economically meaningful after costs.
- Check whether the backtest is truly out-of-sample and whether the evaluation horizon is realistic.
- Record market frictions explicitly rather than treating them as footnotes.

## Typical failure patterns to watch for

- high gross Sharpe with no credible cost model
- in-sample fit presented as tradable alpha
- unreported leverage, capacity, or liquidity constraints
- regime-specific performance oversold as universal
- theoretical market assumptions incompatible with the empirical protocol

## Reusable note prompts

- “The paper is strongest as a model of … rather than a deployable strategy for …”
- “The central finance assumption is …”
- “The backtest is credible / not credible because …”
- “After frictions, the claimed edge is likely …”
