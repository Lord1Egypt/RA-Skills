## Description:

Read your Pooly group wallets — pools, USDC balances on Base, members, spending rules, agents, and spend history — through the official read-only Pooly MCP server. Can simulate a spend; never moves money.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pooly](https://clawhub.ai/user/pooly)

### License/Terms of Use:

MIT-0

## Use Case:

External Pooly users can inspect shared group pools, balances, members, spending rules, authorized agents, and transaction history, or simulate whether a proposed spend fits available funds and limits. The skill does not initiate payments or change wallet settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote MCP connection can expose wallet details to the agent.

Mitigation: Use OAuth through Pooly and confirm the authorization request is limited to pooly.read; never share passwords, recovery phrases, or private keys in chat.

Risk: The optional npx pooly@latest CLI downloads and runs executable code, and its package provenance could not be independently verified.

Mitigation: Prefer the remote MCP connection. If using the CLI, verify its publisher and use a reviewed fixed version.

Risk: Live service behavior and package provenance could not be independently verified.

Mitigation: Treat returned wallet information as unverified service output and confirm important details in the Pooly app.

## Reference(s):

- [Pooly developer documentation](https://www.pooly.org/developer)
- [Pooly ClawHub release](https://clawhub.ai/pooly/skills/pooly)
- [Pooly remote MCP server](https://pooly-be.onrender.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language summaries of wallet information and spend simulations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; simulations do not execute payments. Wallet details may be returned to the agent.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
