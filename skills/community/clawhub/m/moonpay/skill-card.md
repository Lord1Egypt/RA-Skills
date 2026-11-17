## Description:

MoonPay is the crypto onramp for AI agents, supporting wallets, swaps, bridges, transfers, DCA, limit orders, deposits, market data, and fiat on/off ramps via CLI or MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevarifin14](https://clawhub.ai/user/kevarifin14)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let agents operate MoonPay's crypto CLI or local MCP server for wallet management, token trading, deposits, market data, and fiat on/off-ramp workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may perform irreversible financial or wallet operations, including transfers, swaps, bridges, buys, payments, wallet deletion, or mnemonic export.

Mitigation: Require explicit human approval before signing, broadcasting, transferring, bridging, buying, paying, deleting wallets, exporting mnemonics, or installing additional skills.

Risk: Incorrect token addresses, chains, recipients, quotes, fees, or slippage can cause loss of funds.

Mitigation: Manually verify token addresses, chains, recipients, quotes, fees, and slippage before execution, and prefer simulate-then-execute workflows where available.

Risk: The documented global npm install does not pin the @moonpay/cli package version.

Mitigation: Prefer a pinned or otherwise verified @moonpay/cli version and run the skill in an isolated environment with wallets funded only for intended tasks.

## Reference(s):

- [MoonPay Agents](https://agents.moonpay.com)
- [MoonPay ClawHub Skill Page](https://clawhub.ai/kevarifin14/skills/moonpay)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands, MCP configuration, REST API examples, transaction-safety checklists, and operational guidance.]

## Skill Version(s):

0.6.24 (source: server release evidence; artifact frontmatter reports 0.6.23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
