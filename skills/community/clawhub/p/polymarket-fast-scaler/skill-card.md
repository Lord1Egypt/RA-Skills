## Description:

Trades Polymarket BTC 5-minute fast markets using Binance 1-minute momentum, a 0.10% magnitude gate, and conviction-ladder position sizing.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders can use this skill as a reference template for paper-testing and carefully controlled Polymarket BTC 5-minute fast-market automation. It is not evidence of a profitable trading edge and needs review before any live use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money Polymarket orders and may expose the account to irreversible trading losses.

Mitigation: Review live-trading risks first, start in paper mode, and use a dedicated low-balance Simmer account or wallet before considering live execution.

Risk: Account actions and live-run safety controls are under-scoped for unattended operation.

Mitigation: Pin the Simmer SDK version, avoid exposing WALLET_PRIVATE_KEY unless strictly required, and add single-instance control before running any live cron workflow.

Risk: The original performance claim was retracted, and the available signal has no measured edge in the provided evidence.

Mitigation: Treat the strategy as an unvalidated reference template and perform independent paper validation before changing budgets, position sizes, or signal thresholds.

## Reference(s):

- [Polymarket FastScaler ClawHub release](https://clawhub.ai/simmer/skills/polymarket-fast-scaler)
- [Skill documentation](artifact/SKILL.md)
- [Disclaimer](artifact/DISCLAIMER.md)
- [Paper validation results](artifact/paper-validation-results.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance, shell command examples, configuration values, and JSON status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit paper or live trading summaries and automaton telemetry; live mode can place real-money Polymarket orders.]

## Skill Version(s):

1.2.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
