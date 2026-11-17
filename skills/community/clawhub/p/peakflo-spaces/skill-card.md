## Description:

Connect OpenClaw to Spaces by Peakflo, a hosted MCP server for finance and ops work. Hand off one-off or recurring tasks to cloud agents or people, and query workflows, data tables, reports, policy documents and approvals. Sign in with OAuth; no API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peakflo](https://clawhub.ai/user/peakflo)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations teams use this skill to query workspace workflows, reports, data tables, policies, and approvals, or to hand off one-time and recurring work to people or cloud agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some permitted actions can change workspace data or resume workflows with financial effects.

Mitigation: Use read-only tools for queries. Before creating tasks, executing workflows, completing approvals, or changing connected-app or table data, explain the action and obtain explicit user confirmation; call out when an action may move money.

## Reference(s):

- [Spaces MCP documentation](https://spaces.peakflo.ai/docs/mcp/)
- [Spaces MCP source and client configurations](https://github.com/peakflo/spaces-mcp)

## Skill Output:

**Output Type(s):** [API Calls, Text, Shell commands, Configuration instructions]

**Output Format:** [Text responses and Markdown setup guidance, including bash commands and JSON5 configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workspace actions are limited by the connected user's role and permissions.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
