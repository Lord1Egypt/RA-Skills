## Description:

Guides agents through Interactive Brokers CLI setup, connectivity checks, trading workflows, account monitoring, market data, news, options, scanners, and fundamentals using ibkr-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatwang2](https://clawhub.ai/user/fatwang2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate ibkr-cli for Interactive Brokers setup, account checks, market data retrieval, and order workflows from a terminal. It is intended to provide step-by-step command guidance while preserving explicit profile selection and trade preview steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous setup may prefer live Interactive Brokers profiles, exposing real account data or enabling later live trading by mistake.

Mitigation: Use paper profiles by default and choose live profiles only after explicit user intent.

Risk: Trading commands can affect a real brokerage account when submitted against a live profile.

Mitigation: Confirm the target account and preview every trade before any submit command.

Risk: General stock research requests may unintentionally route through brokerage-backed commands.

Mitigation: Use this skill only when the user specifically wants IBKR-backed CLI operations.

## Reference(s):

- [Setup and Connectivity](references/setup.md)
- [Trading and Order Management](references/trading.md)
- [Market Data, News, Options, Scanner, and Fundamentals](references/market-data.md)
- [Account Monitoring and Utilities](references/account.md)
- [IB Gateway download](https://www.interactivebrokers.com/en/trading/ibgateway-stable.php)
- [Trader Workstation download](https://www.interactivebrokers.com/en/trading/tws-updateless-latest.php)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and occasional JSON-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are user-facing command guidance for ibkr-cli and may reference structured JSON responses from the CLI.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
