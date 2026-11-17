## Description:

Helps agents write a Bollinger-band mean-reversion trading strategy for Superior Trade using a 4h timeframe, 2 sigma bands, RSI filters, and ADX range-regime gating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-system builders use this skill to draft a Freqtrade-compatible Bollinger-band mean-reversion strategy, reference futures configuration, and risk framing for range-bound crypto markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The strategy includes short futures trading and backtest claims that may not hold in live markets.

Mitigation: Review and test the trading logic with dry-run or paper trading before using real funds.

Risk: Mean-reversion entries can perform poorly in strong trend regimes.

Mitigation: Use independent risk controls, preserve the documented stop-loss behavior, and evaluate regime filters before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Python and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes strategy mechanics, Freqtrade strategy code, a multi-pair futures reference config, backtest framing, and live-use caution.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
