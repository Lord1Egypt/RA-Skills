## Description:

FastMoss MCP (fastmoss.com). Use this skill for ANY FastMoss MCP request — reading, creating, updating, and deleting data. Whenever a task involves FastMoss MCP, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sellers, and market researchers use the connected FastMoss account to search and analyze TikTok Shop products, creators, shops, videos, advertisements, agencies, and market performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions include remote installer commands whose contents and full effects have not been verified.

Mitigation: Review the CLI installer and install it yourself before allowing setup to run; do not rely on automatic installation.

Risk: FastMoss calls may consume credits, and write or destructive actions may change or remove data.

Mitigation: Inspect the live action schema and behavior annotations, check credit use, and confirm the exact payload and effect before running write or destructive actions.

## Reference(s):

- [FastMoss MCP documentation](https://developer.fastmoss.com/zh/docs/mcp/setup)
- [FastMoss](https://www.fastmoss.com/zh)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [FastMoss MCP on ClawHub](https://clawhub.ai/oomol/skills/oo-fastmoss-mcp)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Shell commands]

**Output Format:** [Text or Markdown analysis and structured JSON connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action and available account data; some calls may consume FastMoss Credits.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
