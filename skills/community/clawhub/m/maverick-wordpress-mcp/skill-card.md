## Description:

Read and write WordPress.com site content through WordPress.com's hosted MCP server. Thin pass-through to WordPress.com's official MCP; the live tool catalog is whatever that server advertises. Use when the user asks about WordPress.com sites, posts, pages, media, comments, or publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

WordPress.com site owners and authorized users can manage posts, pages, media, comments, and publishing workflows through the hosted WordPress.com MCP integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WordPress operations can make public or private changes to site content, including publishing or deleting content.

Mitigation: Confirm clear user intent and check the target site, current state, and intended changes before write actions.

Risk: Setup overwrites stored OAuth values; stale refresh credentials can break the connection after token rotation.

Mitigation: Rerun setup only with fresh credentials, and revoke the OAuth grant when access is no longer needed.

## Reference(s):

- [WordPress.com MCP documentation](https://developer.wordpress.com/docs/mcp/)
- [WordPress.com custom MCP client authentication](https://developer.wordpress.com/docs/mcp/connect-custom-mcp-client/)
- [mcporter configuration reference](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md)

## Skill Output:

**Output Type(s):** [API Calls, Text]

**Output Format:** [WordPress.com content changes and text responses through hosted MCP tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions can create, edit, publish, unpublish, delete, moderate, or upload WordPress.com content, depending on the live tool catalog and account permissions.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
