## Description:

Real-time institutional options flow intelligence and momentum analysis for AI agents using OptionWhales API data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, volatility traders, and quantitative trading teams use this skill to fetch OptionWhales options-flow signals for dashboards, alerts, ticker analysis, and momentum screening across major US equities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an OPTIONWHALES_API_KEY for authenticated OptionWhales API calls.

Mitigation: Install and run it only in environments where that credential is intended to be available, and avoid exposing command output or shell history containing sensitive configuration.

Risk: Options-flow outputs can be mistaken for trading instructions or automated execution signals.

Mitigation: Treat the output as market data analysis and apply independent trading controls before using it in alerts, dashboards, models, or automation.

## Reference(s):

- [OptionWhales API](https://optionwhales.com/api)
- [Options Flow Intelligence on ClawHub](https://clawhub.ai/ssidharhubble/skills/options-flow-intelligence)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command output and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPTIONWHALES_API_KEY for authenticated API calls; no persistence or unrelated local access is reported by security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
