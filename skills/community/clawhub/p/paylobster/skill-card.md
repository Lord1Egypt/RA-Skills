## Description: <br>
PayLobster helps agents use payment infrastructure on Base for treasuries, escrow, token swaps, cross-chain bridges, fiat ramps, identity, reputation, disputes, streaming payments, mandates, and USDC payment workflows through hosted MCP, SDK, CLI, and REST interfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsgustav](https://clawhub.ai/user/itsgustav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use PayLobster to connect agents to real-money payment workflows on Base, including escrows, merchant payments, token swaps, bridges, fiat on/off ramps, identity, reputation, and treasury operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through real-money payment, treasury, escrow, swap, bridge, stream, merchant, subscription, and spend-permission workflows. <br>
Mitigation: Use a dedicated low-balance wallet or testnet first, require explicit confirmation for every transaction, and verify recipient, token, amount, chain, fees, contract address, merchant terms, and subscription terms before execution. <br>
Risk: Prompts, logs, shared configuration, or screenshots could expose private keys or sk_live-style merchant secrets. <br>
Mitigation: Keep private keys and live secrets out of prompts, logs, shared configs, and screenshots. <br>
Risk: Long-lived permissions, streams, subscriptions, treasury roles, and API keys can continue to create financial exposure after setup. <br>
Mitigation: Confirm revocation procedures for spend permissions, streams, subscriptions, treasury roles, and API keys before granting access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/itsgustav/paylobster) <br>
- [PayLobster Website](https://paylobster.com) <br>
- [PayLobster Documentation](https://paylobster.com/docs) <br>
- [Hosted MCP Server](https://paylobster.com/mcp-server) <br>
- [npm SDK: pay-lobster](https://www.npmjs.com/package/pay-lobster) <br>
- [npm CLI: @paylobster/cli](https://www.npmjs.com/package/@paylobster/cli) <br>
- [npm MCP Server: @paylobster/mcp-server](https://www.npmjs.com/package/@paylobster/mcp-server) <br>
- [npm Agent Toolkit: @paylobster/agent-toolkit](https://www.npmjs.com/package/@paylobster/agent-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, TypeScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce transaction, payment, treasury, escrow, bridge, swap, and merchant workflow instructions that require explicit user review before execution.] <br>

## Skill Version(s): <br>
4.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
