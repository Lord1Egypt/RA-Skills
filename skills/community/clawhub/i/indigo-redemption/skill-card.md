## Description:

Manage redemptions and Redemption Order Book (ROB) positions on Indigo Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DeFi operators use this skill to inspect Indigo Protocol redemption queues, review ROB order book liquidity, and prepare unsigned transactions for opening, adjusting, cancelling, claiming, or redeeming ROB positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release uses an unpinned MCP package.

Mitigation: Pin and verify the MCP server version before installation or execution.

Risk: The skill prepares financial transactions without enough built-in safety guidance.

Mitigation: Inspect every unsigned transaction in the wallet before signing, including recipients, assets, amounts, fees, inputs, scripts, and network.

Risk: The security verdict is suspicious.

Mitigation: Review the skill carefully and run it in a constrained environment without unnecessary secrets.

## Reference(s):

- [Indigo Redemption skill page](https://clawhub.ai/adacapo21/skills/indigo-redemption)
- [Redemption MCP Tools Reference](references/mcp-tools.md)
- [Redemption & ROB Concepts](references/concepts.md)
- [Order Book](sub-skills/order-book.md)
- [Redemption Queue](sub-skills/redemption-queue.md)
- [ROB Management](sub-skills/rob-manage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with MCP tool calls, tabular summaries, and unsigned transaction data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations return unsigned Cardano transaction CBOR for client-side signing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
