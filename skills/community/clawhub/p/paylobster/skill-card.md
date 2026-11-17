## Description:

Agent payment infrastructure on Base for hosted MCP, SDK, CLI, and REST workflows covering escrow, treasuries, token swaps, bridges, fiat ramps, identity, reputation, disputes, streaming payments, subscriptions, and USDC payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsgustav](https://clawhub.ai/user/itsgustav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use PayLobster to connect agents to Base payment workflows, including USDC transfers, escrow, subscriptions, service discovery, swaps, bridges, treasury management, and reputation-aware payment checks.

### Deployment Geography for Use:

Global, subject to supported chain, wallet, and fiat-ramp availability.

## Known Risks and Mitigations:

Risk: The skill supports real wallet authority and financial transfers, including payments, swaps, bridges, subscriptions, fiat ramps, and escrow release.

Mitigation: Use low-value dedicated wallets, require manual confirmation for every value-moving action, and prefer hosted or hardware-backed signing instead of raw private keys.

Risk: Private keys, merchant secrets, and payment credentials could be exposed through chat, shell history, logs, or client-side code.

Mitigation: Never place real keys or merchant secrets in prompts, logs, shell history, or browser-delivered code; use secret managers or wallet-backed signing flows.

Risk: Installing or running npm packages can execute third-party code in the agent environment.

Mitigation: Pin package versions, review package provenance and changes before installation, and run payment tooling in a constrained environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itsgustav/skills/paylobster)
- [PayLobster website](https://paylobster.com)
- [PayLobster documentation](https://paylobster.com/docs)
- [PayLobster MCP server](https://paylobster.com/mcp-server)
- [pay-lobster npm package](https://www.npmjs.com/package/pay-lobster)
- [@paylobster/cli npm package](https://www.npmjs.com/package/@paylobster/cli)
- [@paylobster/mcp-server npm package](https://www.npmjs.com/package/@paylobster/mcp-server)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, TypeScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce payment API calls, MCP tool inputs, CLI commands, and integration guidance for financial workflows.]

## Skill Version(s):

4.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
