## Description:

Manage Movedone kanban projects, columns, tasks, comments, and task links via the local HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaichaosun](https://clawhub.ai/user/kaichaosun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate Movedone kanban data from OpenClaw through the local Movedone HTTP API, including project, column, task, comment, and task-link workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bearer token and base URL can provide broad access to local Movedone data.

Mitigation: Keep MOVEDONE_AUTH_TOKEN private and ensure MOVEDONE_BASE_URL points only to the intended local Movedone HTTP API.

Risk: Update and delete commands can change or remove projects, columns, tasks, comments, and task links.

Mitigation: Verify project, column, task, and target task IDs before running data-changing commands.

## Reference(s):

- [Movedone](https://movedone.ai)
- [Movedone download](https://movedone.ai/#download)
- [ClawHub skill page](https://clawhub.ai/kaichaosun/skills/movedone)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with curl command examples and setup notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl plus MOVEDONE_BASE_URL and MOVEDONE_AUTH_TOKEN environment variables.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
