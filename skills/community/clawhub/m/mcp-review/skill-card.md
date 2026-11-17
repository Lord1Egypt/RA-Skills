## Description:

Reviews MCP Server tool implementations against interface design guidelines when users ask to inspect or review tool definitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sawzhang](https://clawhub.ai/user/sawzhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review MCP Server tool definitions against interface design guidelines and produce a structured report with per-tool scores, recurring issues, and concrete fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checklist guidance could be treated as sufficient for high-impact write tools even when those tools need stronger preconditions or confirmation language.

Mitigation: Use the review as a design aid and manually verify that create, update, delete, purchase, or ordering tools require clear user confirmation and state their preconditions.

Risk: The skill reviews tool definition design rather than business logic correctness.

Mitigation: Pair the output with code review, security review, and runtime testing before deploying reviewed MCP servers.

## Reference(s):

- [MCP API Design Guide](artifact/MCP_API_DESIGN_GUIDE.md)
- [McDonald's China MCP platform](https://open.mcd.cn/mcp)
- [McDonald's China MCP Server GitHub](https://github.com/M-China/mcd-mcp-server)
- [Amap MCP Server overview](https://lbs.amap.com/api/mcp-server/summary)
- [Amap MCP Server community GitHub](https://github.com/sugarforever/amap-mcp-server)
- [Model Context Protocol specification](https://spec.modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review report with checklist tables and summary sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output organized by MCP tool, with pass, warning, and fail ratings for ten design criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
