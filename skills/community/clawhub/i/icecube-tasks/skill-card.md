## Description:

IceCube Tasks helps AI agents manage task files across sessions, track progress, handle blockers, and maintain execution continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ares521521-design](https://clawhub.ai/user/ares521521-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent operators use this skill to persist task state in project files, coordinate subtasks and handoffs, track blockers, and resume work after session restarts or context compaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task titles, descriptions, blockers, and history can persist sensitive project or personal information on disk.

Mitigation: Avoid storing secrets or sensitive personal information in task records, and delete state/tasks entries when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ares521521-design/skills/icecube-tasks)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with YAML examples and task-state file conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include persistent task records under state/tasks/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
