## Description:

Work with Jira issue tracking and project workflow state through Atlassian Rovo's hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to review Jira issues and manage project workflow state through Atlassian Rovo MCP. Jira changes should be made only with clear user direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Jira actions can change project data under the connected account's permissions.

Mitigation: Review requested changes and obtain clear user direction before creating, editing, commenting on, or transitioning Jira issues.

Risk: Mishandled OAuth credentials or an active grant can expose Jira access.

Mitigation: Protect stored credentials, rerun setup only with freshly issued OAuth values, and revoke the Atlassian grant when access is no longer needed.

## Reference(s):

- [Atlassian Rovo MCP client setup](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/setting-up-clients/)
- [Atlassian Rovo MCP OAuth 2.1 setup](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/configuring-oauth-2-1/)
- [Atlassian Rovo MCP supported tools](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/)
- [mcporter configuration documentation](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md)
- [ClawHub skill release](https://clawhub.ai/maverick/skills/maverick-jira-mcp)

## Skill Output:

**Output Type(s):** [Text, Analysis, API Calls]

**Output Format:** [Live Jira tool results and concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available tools and result schemas depend on the live Atlassian Rovo MCP server.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
