## Description: <br>
Manage Stability Pool positions on the Indigo Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Indigo Stability Pool state, manage deposits and withdrawals, close positions, and process or cancel pending Stability Pool requests through an Indigo MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fund-moving Stability Pool actions can create unsigned transactions that close, withdraw from, process, or cancel positions. <br>
Mitigation: Before signing, verify the address, asset, amount, UTxO, action type, and expected position effect. <br>
Risk: The skill depends on the configured Indigo MCP server for pool data and transaction construction. <br>
Mitigation: Use only a trusted MCP server and compare returned transaction details with the intended action before signing. <br>


## Reference(s): <br>
- [Indigo Stability ClawHub release](https://clawhub.ai/adacapo21/indigo-stability) <br>
- [Stability Pool MCP Tools Reference](references/mcp-tools.md) <br>
- [Stability Pool Concepts](references/concepts.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration] <br>
**Output Format:** [Markdown guidance with MCP tool calls and unsigned transaction data references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations return unsigned transaction CBOR for client-side review and signing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
