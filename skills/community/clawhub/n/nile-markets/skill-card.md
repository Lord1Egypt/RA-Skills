## Description:

Query Nile Markets, an on-chain FX markets protocol powered by the Open Nile Protocol, starting with non-deliverable forwards (NDFs), through a read-only MCP integration for pool state, positions, oracle prices, and account data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taiyangc](https://clawhub.ai/user/taiyangc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Nile Markets protocol data, including pool health, account positions, oracle prices, fee analytics, token balances, allowances, and trade simulations. It is intended for read-only analysis of Ethereum Sepolia testnet protocol state, not wallet management or on-chain transaction execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and wallet addresses are sent to the configured Nile Markets MCP server.

Mitigation: Use a trusted NILE_MCP_URL endpoint and avoid sending wallet addresses or queries that exceed the user's privacy tolerance.

Risk: The skill is read-only and cannot complete wallet management, transaction signing, transfers, approvals, deposits, withdrawals, or position changes.

Mitigation: Refuse requests for on-chain writes or signing and direct users to the Nile Markets web application or contract tooling for those actions.

Risk: The documented deployment targets Ethereum Sepolia testnet and the API is under active development.

Mitigation: Treat returned market data as testnet information with no real monetary value and verify response freshness before relying on subgraph-sourced results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taiyangc/skills/nile-markets)
- [Nile Markets protocol docs](https://docs.nilemarkets.com)
- [Nile Markets MCP server docs](https://docs.nilemarkets.com/ai-agents/mcp-server)
- [Nile Markets smart contract reference](https://docs.nilemarkets.com/smart-contracts)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text summaries backed by MCP JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only MCP responses include protocol metadata, network information, data payloads, and freshness metadata for subgraph-sourced results.]

## Skill Version(s):

0.3.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
