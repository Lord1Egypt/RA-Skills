## Description:

Analyzes an MCP configuration to estimate tool-schema token usage, identify high-cost tools, and suggest per-role groupings for keeping agent contexts under a target limit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhinas90](https://clawhub.ai/user/abhinas90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit local MCP configs, understand tool-schema token footprint, and plan role-specific MCP server groupings before running subagents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit reads the MCP config file selected by the user.

Mitigation: Run it only against intended local config files and install it only if that access is acceptable.

Risk: Reports may expose private development details such as server names, tool names, paths, and configuration structure.

Mitigation: Review and redact audit output before sharing it outside the intended audience.

Risk: The skill suggests role groupings but does not generate ready-to-use role-specific MCP config files.

Mitigation: Treat groupings as planning guidance and manually create and validate any derived MCP configs.

## Reference(s):

- [MCP Token Auditor on ClawHub](https://clawhub.ai/abhinas90/skills/mcp-token-audit)
- [Publisher profile: abhinas90](https://clawhub.ai/user/abhinas90)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Human-readable audit report or JSON, with command examples in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports estimated token totals, per-server and per-role breakdowns, top token consumers, and suggested role groupings; it does not create ready-to-use role-specific MCP config files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
