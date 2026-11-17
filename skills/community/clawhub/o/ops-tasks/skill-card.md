## Description:

Track tasks with priorities, owners, and statuses for operations teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[admiralkittysdad](https://clawhub.ai/user/admiralkittysdad)

### License/Terms of Use:

MIT-0

## Use Case:

Operations managers and teams use this skill to maintain a concise local task board with priorities, owners, statuses, due dates, and notes. It helps surface overdue tasks, blockers, and critical unassigned P0 work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task titles, owners, due dates, statuses, and notes are stored locally and may contain operationally sensitive information.

Mitigation: Use the skill only on trusted machines with appropriate local storage and backup controls, and avoid putting highly sensitive details in task notes.

Risk: Task-board updates modify a local JSON file.

Mitigation: Follow the skill rule to read the JSON file before writing, and keep backups when the task board is operationally important.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/admiralkittysdad/skills/ops-tasks)
- [Publisher Profile](https://clawhub.ai/user/admiralkittysdad)
- [SkillNexus Homepage](https://skillnexus.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown tables and concise task-management guidance backed by a local JSON task file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local task file at ~/.ops-commander/tasks.json and reads it before writing to reduce data-loss risk.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
