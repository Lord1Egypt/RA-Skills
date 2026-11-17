## Description:

This skill helps agents configure and use gogcli-backed MCP servers for Google Workspace automation across Docs, Sheets, Slides, Drive, and Classroom.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up gogcli MCP servers and route Google Workspace requests for document editing, spreadsheet work, slide authoring, Drive file operations, and Classroom tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to use npm MCP packages with a locally authenticated Google account that may affect real Google Workspace data.

Mitigation: Install only trusted, reviewed package versions and use a dedicated Google account or least-privilege OAuth scopes where possible.

Risk: Generated actions may edit, delete, share, upload, download, or otherwise change Google Workspace resources.

Mitigation: Require explicit confirmation before edits, deletes, permission changes, uploads, downloads, or Classroom actions.

## Reference(s):

- [gogcli repository](https://github.com/chrischall/gogcli)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/gogcli-mcp)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP server configuration snippets, gogcli authentication commands, and task-specific Google Workspace guidance.]

## Skill Version(s):

2.28.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
