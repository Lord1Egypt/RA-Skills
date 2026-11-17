## Description:

Creates cryptocurrency trading bots from natural-language trading styles, runs local backtests, supports reflection-based parameter evolution, and can optionally connect to an external platform for validation and automated trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fei-moss](https://clawhub.ai/user/fei-moss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-strategy developers use this skill to convert natural-language trading styles into BTC/USDT bot parameters, run local or evolved backtests, and optionally upload results or operate live trading through the configured Moss platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store platform API credentials locally for upload and live-trading workflows.

Mitigation: Use a private persistent credential path with restrictive file permissions, avoid shared paths, and rotate any api_secret printed by this version.

Risk: Optional platform features can submit strategy, backtest, credential, or trading requests to an external service.

Mitigation: Enable upload, bind, or live mode only after confirming user intent and verifying the platform URL is the intended HTTPS origin.

Risk: Automated leveraged BTCUSDT trading can create financial loss.

Mitigation: Review backtest results and trading parameters before live mode; require explicit authorization for automatic trading and per-order confirmation in manual mode.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fei-moss/skills/moss-trade-bot-factory)
- [Moss Trader](https://moss.site/agent)
- [Moss Platform API Origin](https://ai.moss.site)
- [Parameter Reference](knowledge/params_reference.md)
- [Evolution Guide](knowledge/evolution_guide.md)
- [Platform Operations](knowledge/platform_ops.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON parameter files, CSV fingerprints, backtest results, upload packages, and live-trading logs when the user authorizes those workflows.]

## Skill Version(s):

1.0.21 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
