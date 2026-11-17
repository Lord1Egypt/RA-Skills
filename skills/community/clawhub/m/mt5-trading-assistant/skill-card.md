## Description:

Comprehensive MetaTrader 5 (MT5) trading automation and monitoring skill for connecting to MT5 platforms, executing trades, monitoring accounts, analyzing market data, and automating trading strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canvascn00-crypto](https://clawhub.ai/user/canvascn00-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading automation users use this skill to connect agents to MetaTrader 5, inspect account and market state, run buy or sell orders, and manage positions through MT5 scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts include reusable MT5 broker credentials.

Mitigation: Remove hardcoded credentials before use, rotate any exposed password, and load account settings from a private config file or environment variables.

Risk: Trade and close-position scripts can submit live MT5 orders without strong confirmation.

Mitigation: Add explicit confirmation or dry-run mode before every trade or close action, and test only with a demo account until the code is reviewed.

Risk: Unpinned runtime dependencies and broker-specific settings can change behavior in a real trading environment.

Mitigation: Pin dependencies, verify broker symbols and servers, and review risk limits before connecting to any non-demo account.

## Reference(s):

- [Config Template](references/config_template.py)
- [Setup Guide](references/setup_guide.md)
- [MetaTrader5 Python Documentation](https://www.mql5.com/en/docs/integration/python_metatrader5)
- [MT5 API Reference](https://www.mql5.com/en/docs/constants/structures)
- [Skill Page](https://clawhub.ai/canvascn00-crypto/skills/mt5-trading-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to run MT5 Python scripts that require a local MT5 desktop client, broker credentials, and AutoTrading enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
