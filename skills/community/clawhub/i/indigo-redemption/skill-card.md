## Description: <br>
Manage redemptions and Redemption Order Book (ROB) positions on Indigo Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Indigo Protocol users and Cardano developers use this skill to inspect ROB order books, review redemption queues, and prepare unsigned ROB management or redemption transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide unsigned blockchain transactions that affect ROB UTxOs and asset movements. <br>
Mitigation: Independently verify the ROB UTxO, address, oracle and iAsset references, amounts, and expected asset movements before signing any transaction. <br>
Risk: Queue timing, fill-rate, and financial estimates may be unreliable without documented data sources. <br>
Mitigation: Treat estimates as advisory only and require a documented data source before using them for financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adacapo21/indigo-redemption) <br>
- [Publisher profile](https://clawhub.ai/user/adacapo21) <br>
- [MCP Tools Reference](references/mcp-tools.md) <br>
- [Redemption Concepts](references/concepts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool calls and unsigned transaction review notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations return unsigned Cardano transaction CBOR for client-side review and signing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
