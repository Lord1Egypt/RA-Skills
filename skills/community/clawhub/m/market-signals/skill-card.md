## Description:

Market Signals analyzes local CSV price data to calculate technical indicators, score market signals, and summarize buy, watch, hold, or avoid suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cqdev-ai](https://clawhub.ai/user/cqdev-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to run local technical analysis on CSV price data, including RSI, moving averages, volume changes, ATR, MACD, Bollinger Bands, VWAP, support/resistance, signal history, and multi-stock scans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market signals and scored recommendations may be mistaken for financial advice.

Mitigation: Treat generated signals as informational technical analysis and review them with appropriate financial judgment before acting.

Risk: Untrusted CSV content may produce misleading terminal or downstream output.

Mitigation: Use trusted CSV files and prefer JSON output when results need to be consumed by other tools.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, guidance]

**Output Format:** [Terminal text reports, optional JSON output, optional JSON files, and ASCII price charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided CSV market data; no external dependencies are declared.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package.json and CHANGELOG.md report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
