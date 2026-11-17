## Description:

Trades Polymarket Bitcoin 5-minute sprint markets using real-time BTC price momentum from Binance. Buys YES when BTC momentum is bullish, NO when bearish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azvn2610](https://clawhub.ai/user/azvn2610)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-automation users use this skill to run or adapt a BTC momentum strategy for Polymarket Bitcoin Up or Down markets. It supports dry-run evaluation by default and live trading only when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money trades.

Mitigation: Keep dry-run mode enabled unless the code has been audited, and use a dedicated, low-limit, revocable Simmer API key for any live deployment.

Risk: Market validation and fail-closed safety checks are weak in the supplied security evidence.

Mitigation: Require stronger market identification and fail-closed context checks before enabling live trading.

Risk: Unpinned dependencies and external market-data APIs can change behavior over time.

Mitigation: Pin dependencies, monitor Binance and Simmer API behavior, and review results before scheduled execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/azvn2610/skills/polymarket-btc-momentum)
- [Binance Klines API](https://api.binance.com/api/v3/klines)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console text with trade reasoning and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; live trading requires --live and SIMMER_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
