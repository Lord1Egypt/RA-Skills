## Description:

Helps an agent use the Polymarket CLI to browse markets, inspect order books and prices, review public wallet and account data, and place or cancel orders with safeguards around wallet and credential handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsnash0](https://clawhub.ai/user/itsnash0)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to operate the `polymarket` CLI for market research, account review, and carefully confirmed trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key listing or credential-related commands may expose account secrets.

Mitigation: Require explicit confirmation before API-key operations and suppress private keys, API secrets, passphrases, and complete credential responses from agent output.

Risk: Trading, cancellation, approval, and on-chain commands can modify financial positions or permissions.

Mitigation: Confirm the exact market or token, side, price, size or amount, and action before execution; use read-only discovery commands first.

Risk: Wallet-management commands and local config files can expose or alter private-key material.

Mitigation: Do not read local private-key config files or run wallet-management commands as the agent; have the user run those commands directly.

## Reference(s):

- [Polymarket CLI command map](references/command-map.md)
- [Polymarket CLI repository](https://github.com/Polymarket/polymarket-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers `-o json` for automation and requires explicit confirmation before sensitive trading, approval, API-key, notification, wallet, or on-chain actions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
