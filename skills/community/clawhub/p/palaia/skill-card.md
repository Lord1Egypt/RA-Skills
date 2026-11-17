## Description:

Local, crash-safe persistent memory for OpenClaw agents with SQLite storage, semantic search, projects, scopes, and auto-capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iret77](https://clawhub.ai/user/iret77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Palaia to add persistent, searchable memory to OpenClaw agents across sessions. It supports local setup, memory capture, recall, project scopes, MCP access, and operational commands for maintaining the memory store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically retain conversation context, tool observations, and session summaries.

Mitigation: Review retention expectations before installation, set autoCapture to false or minimal where appropriate, and use private markers or private scope for sensitive content.

Risk: New entries are shared at team scope by default and public entries can be exported across workspaces.

Mitigation: Change default_scope to private for sensitive work and avoid public scope unless the information is intentionally shareable.

Risk: The skill includes commands for upgrades, doctor --fix, exports, syncs, pruning, deletion, and aggressive garbage collection.

Mitigation: Pin package and plugin versions, require user confirmation before maintenance or destructive commands, and run dry-run modes before exports, imports, pruning, or aggressive cleanup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iret77/skills/palaia)
- [ClawHub publisher profile](https://clawhub.ai/user/iret77)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation, setup, memory operations, maintenance commands, and safety-sensitive cleanup or sharing workflows.]

## Skill Version(s):

2.8.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
