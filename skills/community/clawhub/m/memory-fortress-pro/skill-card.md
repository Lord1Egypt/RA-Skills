## Description:

记忆堡垒(专业版) helps AI agents maintain durable six-layer memory with session state, curated archives, semantic search, Mem0-based extraction, and cloud synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give AI agents persistent memory for project context, preferences, decisions, semantic recall, automatic fact extraction, and optional cloud synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file and shell authority.

Mitigation: Review commands before execution and install only in workspaces where the requested read, write, edit, and shell access is acceptable.

Risk: Automatic memory capture and cloud synchronization can preserve or transmit sensitive personal, business, or secret data.

Mitigation: Avoid storing secrets or sensitive data, constrain or disable automatic extraction where possible, and use cloud sync only for approved workspaces.

Risk: The artifact contains unrelated system administration sections beyond the core memory workflow.

Mitigation: Use only the memory-management behavior unless the unrelated administration capability has been separately reviewed and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memory-fortress-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, configuration examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may reference local files, API-key environment variables, memory stores, optional cloud sync, and automatic extraction behavior.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
