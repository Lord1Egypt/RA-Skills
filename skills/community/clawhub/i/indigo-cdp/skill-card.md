## Description:

Manage Collateralized Debt Positions (CDPs) on the Indigo Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect and manage Indigo Protocol CDPs, including opening positions, adjusting collateral, minting or burning iAssets, analyzing liquidation risk, and preparing unsigned transactions for wallet review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CDP operations such as withdrawal, minting, leverage, liquidation, redemption, freezing, merging, and closing can affect funds and position safety once signed on-chain.

Mitigation: Review every generated transaction in the wallet before signing and confirm collateral ratio, debt, asset, address, and liquidation impact.

Risk: The skill depends on the configured Indigo MCP server for CDP data and unsigned transaction construction.

Mitigation: Install and use it only with an Indigo MCP server that the user trusts for Indigo Protocol workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adacapo21/skills/indigo-cdp)
- [CDP MCP Tools Reference](references/mcp-tools.md)
- [CDP Concepts](references/concepts.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool call parameters, CDP analysis, and unsigned transaction summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations return unsigned CBOR transactions for wallet signing; the skill does not automatically sign transactions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
