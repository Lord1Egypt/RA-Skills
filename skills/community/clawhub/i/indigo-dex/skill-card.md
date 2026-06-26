## Description: <br>
Interact with decentralized exchanges on Cardano through the Indigo Protocol ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Cardano DEX information in the Indigo ecosystem, including SteelSwap token availability and swap estimates, Iris liquidity pools, and Blockfrost wallet balances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet balance lookups can expose wallet addresses and holdings through an external provider. <br>
Mitigation: Do not provide seed phrases, private keys, or wallet addresses you do not want queried through Blockfrost. <br>
Risk: Swap estimates may be treated as transaction approval or final pricing. <br>
Mitigation: Treat estimates as informational only and review current route, price impact, and slippage before any separate transaction. <br>


## Reference(s): <br>
- [DEX Concepts](references/concepts.md) <br>
- [DEX MCP Tools Reference](references/mcp-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, API Calls] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only DEX data queries and informational swap estimates; no transaction execution is described.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
