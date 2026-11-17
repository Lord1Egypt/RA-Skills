## Description:

Mi-MemoryStack helps an OpenClaw agent retrieve and save user memory across conversations through Python command-line tools and a background queue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikol-coder](https://clawhub.ai/user/nikol-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add persistent user-memory retrieval and saving to an OpenClaw agent workflow. It is intended for agents that need conversational continuity, user preferences, or identity context across turns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation turns may be sent to a remote memory service on every interaction.

Mitigation: Use only a trusted HTTPS endpoint, require explicit opt-in, and define retention and deletion controls before deployment.

Risk: API tokens and endpoint configuration may be placed directly in source files.

Mitigation: Move tokens out of source files, restrict file permissions, and load secrets from a managed runtime secret store or environment variables.

Risk: Installation can replace workspace-wide agent instructions and start a persistent background worker.

Mitigation: Review exact diffs before installation, keep rollback backups, and deploy first in an isolated workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nikol-coder/skills/mi-memorystack)
- [Skill definition](artifact/SKILL.md)
- [Installation guide](artifact/安装教程.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include commands that start a persistent memory daemon, queue user conversation content, or call remote memory APIs.]

## Skill Version(s):

1.0.1 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
