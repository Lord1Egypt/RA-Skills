## Description:

Connects an agent to Motion documents so it can read, edit, comment, manage pages and folders, review suggestions, save versions, and export content through Motion's HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[auditt98](https://clawhub.ai/user/auditt98)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document collaborators use this skill to let an agent participate in Motion workspaces, edit documents in suggestion or direct mode, manage pages and folders, handle comments, save versions, and export document content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent tokens grant workspace-wide access to documents, folders, comments, and versions.

Mitigation: Prefer document-scoped invite credentials when possible and install only when the hosted Motion service is trusted with workspace-administrator-level access.

Risk: Tokens may be exposed if pasted into shell commands, chat transcripts, or logs.

Mitigation: Avoid pasting real tokens directly into commands or logs, and revoke any exposed token promptly.

Risk: Direct edits, deletion, page or folder moves, exports, and bulk suggestion accept or reject operations can immediately affect workspace content.

Mitigation: Require explicit user confirmation before these actions, prefer suggestion mode for edits, and save a named version before large destructive changes.

## Reference(s):

- [Motion HTTP API Reference](references/api-reference.md)
- [ProseMirror Block & Mark Reference](references/block-format-reference.md)
- [Common Workflow Examples](references/examples.md)
- [Motion MCP Server API](https://motion-mcp-server.fly.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP API request examples, JSON payloads, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce live document mutations through Motion API calls when the user provides valid credentials and confirms the intended action.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
