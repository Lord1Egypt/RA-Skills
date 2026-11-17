## Description:

Memory Layered defines a six-layer, file-based memory architecture for AI agents to persist, retrieve, consolidate, and forget user preferences, project state, reusable skills, and lessons across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheyuy](https://clawhub.ai/user/sheyuy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add durable, file-based memory for agents that need continuity across sessions, shared project context, or structured user preference tracking without overloading the active context window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally maintains durable local memory, which can retain personal or project information longer than a single session.

Mitigation: Decide which categories of information may be stored before use, avoid sensitive data unless explicitly needed, and periodically review memory/topics and memory/.learnings.

Risk: Forgetting or archiving routines could remove useful long-term context if applied without review.

Mitigation: Require confirmation before pruning or archiving important memory entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sheyuy/skills/memory-layered)
- [Server-resolved GitHub provenance](https://github.com/Sheyuy/agent-skills/tree/main/skills/memory-layered)
- [Botlearn homepage](https://www.botlearn.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation and maintenance of local memory files including memory/memory.md, memory/topics, memory/SESSION-STATE.md, and memory/.learnings.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
