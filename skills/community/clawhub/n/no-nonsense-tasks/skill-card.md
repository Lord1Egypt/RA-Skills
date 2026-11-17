## Description:

No-nonsense task manager using SQLite. Track tasks with statuses (backlog, todo, in-progress, done), descriptions, and tags. Use when managing personal tasks, to-do items, project tracking, or any workflow that needs status-based task organization. Supports adding, listing, filtering, updating, moving, and deleting tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dvjn](https://clawhub.ai/user/dvjn)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to maintain a local SQLite task list with statuses, descriptions, tags, filtering, updates, statistics, and delete operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and modifies a local SQLite task database under the user's home directory by default.

Mitigation: Review the database location before initialization and set NO_NONSENSE_TASKS_DB to a preferred path when the default is not appropriate.

Risk: The delete command removes task records rather than archiving them.

Mitigation: Confirm task IDs before deletion and back up or export the database when task history must be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dvjn/skills/no-nonsense-tasks)
- [Usage guide](SKILL.md)
- [Development guide](AGENT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise task-management guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of local Bash scripts backed by a SQLite database.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
