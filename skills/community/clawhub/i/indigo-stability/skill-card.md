## Description:

Manage Stability Pool positions on the Indigo Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT-0

## Use Case:

External Cardano and Indigo Protocol users use this skill to inspect stability pools, manage pool accounts, and prepare unsigned transactions for deposits, withdrawals, account closure, and pending request processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prepared transactions can move funds or change Indigo Stability Pool positions if the user signs them without review.

Mitigation: Review the asset, amount, address, UTxO, and expected effect in the wallet before signing any transaction.

Risk: The skill depends on the @indigoprotocol/indigo-mcp server for protocol data and unsigned transaction construction.

Mitigation: Use a trusted or audited MCP server and verify pool, account, and pending request details before submitting transactions.

Risk: iAsset amounts must be provided in smallest units, which can cause incorrect deposit or withdrawal amounts if decimal precision is misapplied.

Mitigation: Confirm decimal conversion for iUSD, iBTC, iETH, and iSOL before creating or adjusting a stability pool account.

## Reference(s):

- [Stability Pool Concepts](references/concepts.md)
- [MCP Tools Reference](references/mcp-tools.md)
- [ClawHub Skill Page](https://clawhub.ai/adacapo21/skills/indigo-stability)

## Skill Output:

**Output Type(s):** [guidance, text, API calls, configuration]

**Output Format:** [Markdown or text with structured MCP tool-call parameters; write operations return unsigned Cardano transaction CBOR for wallet review and signing.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the @indigoprotocol/indigo-mcp server; amounts use each iAsset's smallest unit.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
