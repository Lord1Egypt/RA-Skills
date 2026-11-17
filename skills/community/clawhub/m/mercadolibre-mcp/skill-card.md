## Description:

Complete MCP server for Mercado Libre seller operations: products, orders, pricing, stock, questions, ads, reputation, and competitor analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosnahuel](https://clawhub.ai/user/marcosnahuel)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, developers, and operators use this MCP server to inspect and manage Mercado Libre seller operations from an agent client. It supports product, order, pricing, inventory, question, ads, reputation, metrics, competitor, and category workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server can make live seller-account changes, including listing prices, inventory, public question answers, and ads.

Mitigation: Use restricted or test credentials where possible and require human confirmation in the MCP host before write tools execute.

Risk: Refresh-token material may be partially logged.

Mitigation: Protect logs, limit log access, and rotate Mercado Libre tokens if existing logs may contain token fragments.

Risk: Dependencies may need review before production deployment.

Mitigation: Update and audit dependencies before using the server in a production seller account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcosnahuel/skills/mercadolibre-mcp)
- [Project homepage](https://github.com/MarcosNahuel/mercadolibre-mcp)
- [Mercado Libre developer documentation](https://developers.mercadolibre.com)
- [TRAID](https://traid.ai)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [MCP tool responses as text or markdown, with setup guidance and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Mercado Libre seller credentials and may return live account, listing, order, advertising, question, reputation, and competitor data.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
