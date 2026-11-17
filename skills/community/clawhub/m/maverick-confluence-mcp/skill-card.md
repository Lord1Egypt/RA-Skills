## Description:

Work with Confluence workspace content through Atlassian Rovo's hosted MCP server. Thin pass-through to Atlassian's official MCP; the live tool catalog is whatever that server advertises. Use when the user asks about Confluence pages, spaces, docs, comments, or knowledge-base updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Confluence users can find, read, search, and manage workspace pages, spaces, comments, and knowledge-base content through Atlassian Rovo. The user should authorize specific content changes before the skill performs them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confluence operations can create, update, publish, or comment on content using the connected user's permissions.

Mitigation: Use read and search operations for gathering context; make a specific content change only after clear user intent and authorization.

Risk: Tool arguments and results transit Atlassian's hosted MCP service.

Mitigation: Send only information relevant to the requested Confluence task and avoid passing unrelated sensitive content.

Risk: OAuth credentials are stored for reuse, and rerunning setup with stale credentials can overwrite a rotated refresh token.

Mitigation: Protect stored credentials, rerun setup only with freshly issued OAuth credentials, and revoke the Atlassian grant when the integration is no longer needed.

## Reference(s):

- [Atlassian Rovo MCP setup](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/setting-up-clients/)
- [Atlassian Rovo MCP OAuth configuration](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/configuring-oauth-2-1/)
- [Atlassian Rovo MCP supported tools](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/)
- [mcporter configuration documentation](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text or Markdown; structured results depend on the selected Confluence tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content and available operations depend on the live Atlassian Rovo MCP tool catalog and the connected user's Confluence permissions.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
