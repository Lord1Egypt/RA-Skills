## Description:

Prismer enables agents to fetch and compress web context, parse documents with OCR, exchange messages, manage tasks and memory, share files, and use evolution workflows through CLI and SDK interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ooxxxxoo](https://clawhub.ai/user/ooxxxxoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Prismer to add cloud-backed knowledge retrieval, document parsing, agent messaging, persistent memory, task coordination, file sharing, and shared evolution learning to agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents toward unpinned package and plugin execution.

Mitigation: Install only from trusted Prismer package and plugin sources, prefer pinned versions or a reviewed lockfile, and review installation commands before execution.

Risk: The skill supports persistent memory, file sharing, and cloud-backed data handling.

Mitigation: Avoid uploading sensitive files unless intentional, treat memory entries as retained cloud data, and delete files or memories that should not persist.

Risk: The skill uses API keys, webhook secrets, JWTs, and identity credentials.

Mitigation: Protect secrets, avoid placing credentials in shared transcripts or committed files, and rotate or refresh tokens when access is uncertain.

Risk: The skill can install or sync catalog skills locally.

Mitigation: Inspect catalog skill contents before installing or syncing them into an agent workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ooxxxxoo/skills/global-agent-node-with-real-time-context-streaming-mission-form-autonomous-network-status-awaiting-peers)
- [Prismer Cloud Documentation](https://prismer.cloud/docs)
- [Prismer Cloud](https://prismer.cloud)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, SDK code examples, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance may include external service calls, persistent memory operations, file uploads, and package or plugin installation steps.]

## Skill Version(s):

1.7.4 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
