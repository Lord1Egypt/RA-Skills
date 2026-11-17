## Description:

Provides Korean crypto market, exchange, sentiment, and news data through paid MCP and REST endpoints with AI analysis, x402 payments, and signed receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bakyang2](https://clawhub.ai/user/bakyang2)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to query South Korean crypto premiums, exchange signals, Korean market sentiment, and translated Korean news for trading or content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid remote calls may incur per-call charges when the MCP client approves x402 payment.

Mitigation: Review payment approval settings, use user-invoked mode, and configure spending limits before installation.

Risk: Tool calls may send requested topic parameters and standard HTTP metadata to the remote service.

Mitigation: Review the MCP client's privacy and transport settings before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bakyang2/skills/kr-crypto-intelligence)
- [API documentation](https://api.printmoneylab.com/docs)
- [MCP server endpoint](https://mcp.printmoneylab.com/mcp)
- [Artifact-provided public repository link](https://github.com/bakyang2/kr-crypto-intelligence)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis]

**Output Format:** [Markdown guidance and JSON-like MCP or REST responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid responses may include signed receipt metadata for agent accountability.]

## Skill Version(s):

1.5.0 (source: evidence release and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
