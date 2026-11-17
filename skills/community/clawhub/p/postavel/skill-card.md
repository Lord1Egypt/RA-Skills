## Description:

Connect to Postavel social media management platform via MCP (Model Context Protocol) to create, schedule, and manage social media posts across Facebook, Instagram, and LinkedIn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nezaboravi](https://clawhub.ai/user/nezaboravi)

### License/Terms of Use:


## Use Case:

External users and social media teams use this skill to connect an assistant to a Postavel account, manage workspaces and brands, draft posts, schedule content, review calendars, and run approval workflows through natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include remote installer and privileged or global binary installation paths.

Mitigation: Prefer the manual setup path, inspect scripts before running them, and avoid curl-to-bash, sudo downloads, or global package installation unless the source has been independently verified.

Risk: The connected Postavel account may be able to publish, approve, auto-approve, or delete social media content.

Mitigation: Confirm the workspace, brand, target platforms, post content, schedule, and publishing action before approving or executing changes.

Risk: OAuth configuration grants an assistant access to account resources allowed by the user's Postavel permissions.

Mitigation: Use least-privilege Postavel roles, review connected workspaces and brands, and revoke access from Postavel settings when the connection is no longer needed.

## Reference(s):

- [Postavel skill page](https://clawhub.ai/nezaboravi/skills/postavel)
- [Postavel MCP tools reference](references/mcp-tools.md)
- [Postavel MCP setup guide](references/setup-guide.md)
- [Postavel MCP server endpoint](https://postavel.com/mcp/postavel)
- [mcporter project](https://github.com/steipete/mcporter.git)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, text]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and natural-language action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OAuth authentication and user confirmation for publishing, approval, and deletion actions.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
