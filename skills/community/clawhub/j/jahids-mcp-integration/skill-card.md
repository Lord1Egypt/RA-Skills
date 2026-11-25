## Description:

Design and review Model Context Protocol tool integrations with scoped access, validation, approvals, and auditable execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mdjahid11978-design](https://clawhub.ai/user/mdjahid11978-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when connecting an MCP server or tool provider to the JAHIDS MCP Gateway. It guides them in defining scoped access, validating requests, requiring approvals for consequential actions, and documenting audit requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An MCP integration may expose sensitive or consequential tool actions.

Mitigation: Apply per-tenant and per-workspace allowlists, keep credentials in a secret manager, route consequential calls through Governor approval, and record auditable execution details.

Risk: Tool descriptions and outputs may contain untrusted or misleading instructions.

Mitigation: Treat tool descriptions and outputs as untrusted data rather than policy instructions, and validate arguments against defined schemas before invocation.

## Reference(s):

- [Imported source on GitHub](https://github.com/mdjahid11978-design/Jahids-skills/tree/main/skills/jahids-mcp-integration)
- [ClawHub skill page](https://clawhub.ai/mdjahid11978-design/skills/jahids-mcp-integration)
- [Publisher profile](https://clawhub.ai/user/mdjahid11978-design)

## Skill Output:

**Output Type(s):** [Configuration, Guidance, Test plans, Audit requirements]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contents vary with the integration being reviewed.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
