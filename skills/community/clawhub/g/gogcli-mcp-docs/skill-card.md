## Description:

Use when the user asks to read, write, edit, export, or comment on Google Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to connect an agent to Google Docs for reading, editing, exporting, tab management, and comment workflows through the gogcli MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change, remove, trash, replace, or delete content in Google Docs.

Mitigation: Use a dedicated low-privilege Google account, review Docs version history or backups before large edits, and require explicit confirmation before destructive document or comment operations.

Risk: The setup installs the MCP package through an unpinned npm invocation.

Mitigation: Install only from a trusted package source and prefer pinning the npm package version before deployment.

## Reference(s):

- [gogcli](https://github.com/openclaw/gogcli)
- [gogcli-mcp source](https://github.com/chrischall/gogcli-mcp)
- [gogcli issue 607](https://github.com/openclaw/gogcli/issues/607)
- [gogcli issue 608](https://github.com/openclaw/gogcli/issues/608)
- [gogcli issue 609](https://github.com/openclaw/gogcli/issues/609)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/gogcli-mcp-docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON configuration and inline tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute Google Docs read, edit, export, formatting, tab, and comment operations through the configured MCP server.]

## Skill Version(s):

2.8.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
