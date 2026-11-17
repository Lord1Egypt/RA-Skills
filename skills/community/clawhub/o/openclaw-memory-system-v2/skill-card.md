## Description:

OpenClaw记忆管理系统v2 defines a three-layer local memory workflow using NOW.md, daily logs, and a structured knowledge base with heartbeat writes, nightly reflection, CRUD validation, and active forgetting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muisenice](https://clawhub.ai/user/muisenice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain persistent local working memory, daily activity logs, and reusable knowledge files across OpenClaw sessions. It is intended for ongoing personal or project context management where regular review and redaction practices are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to scan sessions and persist personal or sensitive context in local memory files.

Mitigation: Restrict which sessions can be scanned, avoid storing secrets or private personal data, and review memory changes regularly.

Risk: The skill does not provide built-in deletion, redaction, or backup practices for persisted memory.

Mitigation: Add explicit deletion, redaction, and backup procedures before operational use.

## Reference(s):

- [OpenClaw记忆管理系统v2 on ClawHub](https://clawhub.ai/muisenice/skills/openclaw-memory-system-v2)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with file paths, schedules, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for local memory files; does not itself provide deletion, redaction, backup, or access controls.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
