## Description:

Complete memory management tool to activate, organize, and back up an AI agent's local memory folder; must be paired with memory-key for full function.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to structure local cross-session memory into hot, warm, and cold storage so an agent can reload priorities, principles, completed work, and archived conversations across restarts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to persist and reload sensitive conversation-derived memory, including broad backup and archival behavior.

Mitigation: Review before installing, exclude secrets and sensitive personal or business data, and add explicit approval, redaction, encryption, retention, and deletion controls where needed.

Risk: Cold storage preserves raw conversation archives without deletion or minimization by default.

Mitigation: Define retention limits and deletion procedures before enabling archival workflows.

## Reference(s):

- [Memory Treasure on ClawHub](https://clawhub.ai/markma84/skills/memory-treasure)
- [Memory concept template](artifact/examples/memory/00-概念模板.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown instructions and directory conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory organization guidance, startup loading expectations, storage rules, and backup behavior.]

## Skill Version(s):

4.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
