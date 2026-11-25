## Description:

Keep a small synthetic task list in persistent SQLite, with explicit add, list and complete operations and no network access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsichenwang](https://clawhub.ai/user/hsichenwang)

### License/Terms of Use:

MIT

## Use Case:

People using an AI assistant can save non-sensitive tasks, review the saved list, and mark a task complete by its returned ID. The skill does not schedule reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool scope is undeclared, so the host runtime's enforcement of the helper's Python and shell capabilities is not established.

Mitigation: Review the host execution policy before running the local helper, and store only non-sensitive task titles.

## Reference(s):

- [A3 Task Memory on ClawHub](https://clawhub.ai/hsichenwang/skills/hsichenwang-task-memory)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Task records and status in JSON or concise text; shell commands for the local helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists show up to 30 tasks; storage is limited to 500 tasks and titles to 250 characters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
