## Description:

Trade on GRVT (Gravity Markets) derivatives exchange via the grvt-cli tool for market data, account review, order management, leverage changes, transfers, and withdrawals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madeinusmate](https://clawhub.ai/user/madeinusmate)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate the GRVT CLI for crypto derivatives trading workflows, including market analysis, portfolio checks, order placement and cancellation, leverage management, transfers, and withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an unaudited CLI with live exchange credentials, private-key signing, fund movement, withdrawals, and confirmation bypasses.

Mitigation: Use testnet or low-value accounts, avoid production funds unless the exact CLI version has been audited, and prefer restricted credentials that cannot withdraw assets.

Risk: Passing real API keys or private keys as command-line arguments can expose credentials, and --yes can bypass confirmations for trading or fund-moving commands.

Mitigation: Do not pass real API keys or private keys as command-line arguments, require explicit user acknowledgement before risky actions, avoid --yes on trading or fund-moving commands, and use dry-run previews where available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/madeinusmate/skills/grvt-markets-agent-skill)
- [Config & Auth Commands](references/commands-config.md)
- [Market Data Commands](references/commands-market.md)
- [Trading Commands](references/commands-trade.md)
- [Account Commands](references/commands-account.md)
- [Fund Management Commands](references/commands-funds.md)
- [Error Codes and Troubleshooting](references/errors.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and CLI output formats including table, JSON, NDJSON, and raw API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that authenticate to GRVT, sign requests, place or cancel orders, transfer funds, or withdraw assets when explicitly authorized.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
