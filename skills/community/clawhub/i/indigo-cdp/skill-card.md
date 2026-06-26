## Description: <br>
Manage Collateralized Debt Positions (CDPs) on the Indigo Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect and manage Indigo Protocol CDPs, including opening positions, depositing or withdrawing collateral, minting or burning iAssets, checking health, and preparing unsigned Cardano transactions for wallet signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prepared DeFi transactions can move collateral, mint or burn assets, liquidate positions, or alter leverage. <br>
Mitigation: Review the CDP reference, asset, amount, fees, collateral ratio, liquidation risk, and wallet transaction details before signing. <br>
Risk: The skill depends on an external Indigo MCP server for CDP data and unsigned transaction preparation. <br>
Mitigation: Use only a trusted Indigo MCP server and independently verify transaction contents in the Cardano wallet before submission. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/adacapo21/indigo-cdp) <br>
- [Publisher profile](https://clawhub.ai/user/adacapo21) <br>
- [MCP Tools Reference](references/mcp-tools.md) <br>
- [CDP Concepts](references/concepts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls, Configuration] <br>
**Output Format:** [Markdown with tool call parameters and unsigned transaction details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations return unsigned Cardano transaction CBOR for user wallet signing.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
