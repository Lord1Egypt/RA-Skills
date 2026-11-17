## Description:

Users describe a trading style in natural language, and the skill creates a crypto trading bot, runs local backtests, supports periodic reflection-driven evolution, and can optionally connect to an external platform for verification and simulated live trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fei-moss](https://clawhub.ai/user/fei-moss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-strategy builders use this skill to turn natural-language crypto trading ideas into parameterized bot configurations, local backtests, and concise strategy results. It can also guide optional verification upload and simulated live trading when the user explicitly enables platform features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist platform credentials and use them for authenticated platform requests.

Mitigation: Use only a trusted HTTPS platform origin, protect ~/.moss-trade-bot/agent_creds.json with owner-only permissions, avoid passing secrets on the command line, and enable platform features only after explicit user intent.

Risk: The skill can upload strategy and backtest data to an external platform.

Mitigation: Review generated parameters, backtest outputs, and upload contents before submitting verification data to the user-specified platform.

Risk: The skill can run an automated simulated trading loop when enabled.

Mitigation: Review auto-trading and auto-resubmission behavior before enabling it, and require explicit authorization before starting auto mode.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fei-moss/skills/moss-trade-bot-factory-en)
- [Moss Trader Platform](https://moss.site/agent)
- [Parameter Reference](knowledge/params_reference.md)
- [Evolution Guide](knowledge/evolution_guide.md)
- [Platform Operations Manual](knowledge/platform_ops.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON parameter files and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local parameter, fingerprint, backtest, evolution, and upload-package files while guiding the agent workflow.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
