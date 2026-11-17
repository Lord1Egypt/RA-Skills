## Description:

Trade on Phemex (USDT-M futures, Coin-M futures, Spot) - place orders, manage positions, check balances, and query market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bubble501](https://clawhub.ai/user/bubble501)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Phemex market data, inspect account state, place or modify orders, manage positions and leverage, and transfer funds through phemex-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can exercise real financial authority through trading, order cancellation, leverage changes, position-mode changes, and transfers.

Mitigation: Require explicit user confirmation before actions that trade, cancel, change leverage, switch modes, or move funds; start on testnet and show account and position context before trading.

Risk: Persistent exchange credentials may be stored in ~/.phemexrc as plaintext.

Mitigation: Prefer an OS secret store or ephemeral environment variables; if ~/.phemexrc is used, restrict file access to the current user and use a dedicated least-privileged Phemex API key without withdrawal permissions.

Risk: A mutable global CLI install can change behavior between runs.

Mitigation: Install a pinned and audited phemex-trade-mcp version before use and review changes before upgrading.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bubble501/skills/phemex-trade)
- [Project Homepage Listed in Artifact](https://github.com/betta2moon/phemex-trade-mcp)
- [Phemex](https://phemex.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses phemex-cli; authenticated account, trading, leverage, position-mode, and transfer operations require PHEMEX_API_KEY and PHEMEX_API_SECRET.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
