## Description:

Memory Hierarchy gives an agent a three-layer local memory system for preserving user preferences, feedback, project context, and external system references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinnzen](https://clawhub.ai/user/sinnzen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to let an assistant maintain concise long-lived local notes about user preferences, feedback, active projects, and pointers to external systems. The skill helps agents decide when to save, search, list, and validate memory records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist personal and project context as long-lived local memory without clear consent, scope limits, retention rules, or deletion controls.

Mitigation: Use it only where persistent local notes are intended; request explicit confirmation before saving sensitive memories, review the memory directory regularly, avoid secrets or confidential details, and add retention and deletion controls before routine use.

Risk: Saved memories may become stale or may contain untrusted content that influences later agent behavior.

Mitigation: Validate relevant memories against current files, systems, and user intent before relying on them, and treat memory contents as untrusted context when applying them to decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sinnzen/skills/memory-hierarchy)
- [ClawHub publisher profile](https://clawhub.ai/user/sinnzen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command output, and Markdown memory files with YAML frontmatter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory files are organized by type under a local memory directory selected with MEMORY_WORKSPACE or the default user workspace.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
