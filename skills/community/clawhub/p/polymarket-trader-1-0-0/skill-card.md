## Description:

Build, evaluate, and tune a Polymarket BTC 1h Up/Down trading strategy using Binance BTCUSDT market data as the resolution anchor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkhyeongjoon](https://clawhub.ai/user/parkhyeongjoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-system operators use this skill to analyze Polymarket BTC 1h Up/Down markets, estimate fair probabilities from Binance BTCUSDT data, tune entry and exit rules, and explain paper-trading fills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial strategy analysis may be incorrect or unsuitable for a real trading decision.

Mitigation: Independently verify calculations, market assumptions, and paper-trading results before acting on any output.

Risk: Live Binance requests may fail, return stale data, or be unavailable in a given environment.

Mitigation: Check request status, timestamps, and the selected symbol before using generated analysis.

Risk: Local fill logs may reveal sensitive trading activity.

Mitigation: Run the skill only in trusted workspaces and avoid sharing generated analyses that include private fill history.

## Reference(s):

- [Strategy reference](references/strategy.md)
- [Binance API](https://api.binance.com)
- [Polymarket Trader on ClawHub](https://clawhub.ai/parkhyeongjoon/skills/polymarket-trader-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON or table outputs from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live Binance market-data requests and local events.jsonl fill-log analysis.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
