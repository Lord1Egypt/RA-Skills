## Description:

Interact with decentralized exchanges on Cardano through the Indigo Protocol ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Cardano DEX information in the Indigo ecosystem, including SteelSwap token lists and swap estimates, Iris liquidity pools, and Blockfrost wallet balances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet balance lookups send the queried Cardano address to Blockfrost and can reveal holdings associated with that address.

Mitigation: Avoid querying addresses you do not want associated with your usage, and review responses before sharing them.

Risk: DEX estimates, liquidity data, and wallet balances can become stale or incomplete because they depend on third-party Cardano data services.

Mitigation: Treat outputs as informational and verify market data with trusted services before making trading or portfolio decisions.

## Reference(s):

- [DEX MCP Tools Reference](references/mcp-tools.md)
- [DEX Concepts](references/concepts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown text with structured DEX data and MCP tool call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Cardano DEX and wallet-balance queries; balance lookups send wallet addresses to Blockfrost.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
