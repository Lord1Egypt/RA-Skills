## Description:

Automates Binance Futures signal detection, leveraged order entry, stop-loss/take-profit monitoring, Telegram notifications, and a local trading dashboard for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukmanc405](https://clawhub.ai/user/lukmanc405)

### License/Terms of Use:

MIT-0

## Use Case:

External developers or agents use this skill to run and inspect an automated Binance Futures trading workflow, including signal scanning, position monitoring, Telegram alerts, and dashboard status checks. It is intended for users who understand leveraged trading and can manage exchange credentials securely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute automated leveraged Binance Futures trades with real funds.

Mitigation: Use only test or tightly scoped, IP-restricted Binance keys and fix order-management issues before using real funds.

Risk: The dashboard can expose account and position data if reachable from a public network.

Mitigation: Do not expose the dashboard publicly; keep it on a private interface or behind strong access controls.

Risk: Credential handling depends on local environment files and the artifact includes a command that prints part of .env.

Mitigation: Remove any instruction that prints .env contents and rotate Binance or Telegram credentials if the code or dashboard has run on an exposed host.

Risk: Server security review flagged serious issues around secret handling, public dashboard exposure, and automatic order execution.

Mitigation: Review before installing and resolve the security guidance before production or real-funds use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lukmanc405/skills/neko-futures-trader)
- [ClawHub publisher profile](https://clawhub.ai/user/lukmanc405)
- [Binance Futures](https://www.binance.com/en/futures)
- [TradingView chart link used in alerts](https://www.tradingview.com/chart/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Text, API calls, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, environment variable requirements, status text, Telegram message templates, and JSON dashboard responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 plus Binance and Telegram credentials; may issue live Binance Futures API calls when executed.]

## Skill Version(s):

1.0.27 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
