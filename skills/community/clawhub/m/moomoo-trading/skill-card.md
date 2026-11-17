## Description:

Use OpenD-backed moomoo/Futu scripts for quotes, K-lines, price alerts, portfolio/account checks, and stock order execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobbythebot2008-beep](https://clawhub.ai/user/bobbythebot2008-beep)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query moomoo/Futu market data, inspect account and portfolio state, monitor price thresholds, and place or manage stock orders through an OpenD gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place, modify, or cancel real securities orders when explicitly invoked.

Mitigation: Use simulated trading by default, require explicit live-trading confirmation, and verify account, ticker, quantity, price, and market before any real order action.

Risk: A live-trading unlock password can be sent to any configured OpenD host.

Mitigation: Keep live trading pointed at a trusted local OpenD instance and avoid remote host values unless they are protected by a secure authenticated tunnel.

Risk: Setup and account checks may expose financial account identifiers.

Mitigation: Do not share setup_check.py output or account-query output in public channels, issue trackers, or logs.

Risk: The live-trading unlock password is sensitive credential material.

Mitigation: Store it only in an environment variable, avoid putting it on the command line, and protect the environment where the skill runs.

## Reference(s):

- [Futu / moomoo OpenAPI Reference](references/api-reference.md)
- [moomoo / Futu OpenD Setup Guide](references/setup-guide.md)
- [Futu OpenAPI Documentation](https://openapi.futunn.com/futu-api-doc/en/)
- [moomoo OpenAPI Documentation](https://openapi.moomoo.com/moomoo-api-doc/en/)
- [moomoo OpenAPI Download](https://www.moomoo.com/download/OpenAPI)
- [ClawHub Skill Page](https://clawhub.ai/bobbythebot2008-beep/skills/moomoo-trading)
- [ClawHub Publisher Profile](https://clawhub.ai/user/bobbythebot2008-beep)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke OpenD-backed quote, portfolio, watchlist, and trade scripts when the user has configured the local SDK and gateway.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
