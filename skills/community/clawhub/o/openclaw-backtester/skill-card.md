## Description:

OpenClaw Backtester helps agents run local trading strategy backtests for SMA crossover, RSI, MACD, and Bollinger Bands strategies and report performance metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cry779](https://clawhub.ai/user/cry779)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading practitioners use this skill to validate and compare trading strategy ideas against historical local OHLCV data before considering live deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backtest results may be inaccurate or misleading if calculations, dependencies, or input data quality are not independently checked.

Mitigation: Validate the strategy logic, performance calculations, installed dependencies, and source data before using results to make trading decisions.

Risk: The skill depends on a disclosed local OpenClaw SQLite trading database and may fail or produce incomplete results when that database is missing or sparse.

Mitigation: Confirm the local database path exists, contains the requested symbol and date range, and has clean OHLCV records before running comparisons.

Risk: The documentation overstates some features relative to the scanner summary, which can create false confidence in strategy validation.

Mitigation: Treat outputs as advisory analysis, paper trade separately, and verify any advertised feature before relying on it in a workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cry779/skills/openclaw-backtester)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text backtest results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a local OpenClaw trading SQLite database; backtest results should be independently validated before use in trading decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
