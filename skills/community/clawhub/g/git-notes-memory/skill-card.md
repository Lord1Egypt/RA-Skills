## Description:

Git-Notes-Based knowledge graph memory system for branch-aware storage and retrieval of Claude Code project context, decisions, tasks, and learnings across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mourad-ghafiri](https://clawhub.ai/user/mourad-ghafiri)

### License/Terms of Use:

MIT

## Use Case:

Developers and Claude Code users use this skill to give an agent local, branch-aware project memory for continuity across sessions. It supports storing, retrieving, updating, and organizing context such as decisions, preferences, tasks, and learnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to store and reuse project context silently, which can preserve information without clear user consent.

Mitigation: Enable it only in repositories where automatic local memory is acceptable and avoid using it around secrets or confidential material unless opt-in, visible logging, path scoping, and review/delete controls are added.

Risk: The skill makes persistent Git notes changes in local repositories.

Mitigation: Use it only where silent Git mutations are acceptable, and ensure collaborators understand that Git notes may contain project context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mourad-ghafiri/skills/git-notes-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON memory payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The memory tool returns compact JSON for session context, topic lookup, and full memory recall.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
