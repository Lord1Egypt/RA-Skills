## Description:

Complete memory management system for OpenClaw agents. Combines compaction-aware saving, a formal boot sequence, domain organization, memory scoring, structured learnings, and documentation-first project continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wroadd](https://clawhub.ai/user/wroadd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Memory Fortress to give OpenClaw agents a file-based memory workflow for preserving task state, decisions, preferences, and project continuity across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to persist broad user and conversation data across sessions.

Mitigation: Scope what may be saved before use, avoid exact quotes for sensitive requests, and apply redaction and retention rules.

Risk: Copying the workflow into a global agent manual could make broad persistence the default for unrelated work.

Mitigation: Install it only where a durable file-based memory workflow is intended and keep project-specific memory separated from global agent rules.

Risk: The memory workflow has insufficient rollback controls for stale or incorrect saved context.

Mitigation: Review state, memory, and domain files periodically, mark stale entries explicitly, and keep closed decisions separate from active task state.

## Reference(s):

- [Memory Fortress ClawHub release page](https://clawhub.ai/wroadd/skills/memory-fortress)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces conventions for state files, daily logs, domain memory files, project documentation, and reorientation snapshots.]

## Skill Version(s):

1.1.2 (source: frontmatter, changelog, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
