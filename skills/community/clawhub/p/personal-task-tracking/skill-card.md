## Description:

Query and manage ClickUp via REST API and the local `scripts/query.sh` helper. Use when listing open or completed tasks, counting due work, looking up spaces or lists, checking assignee workload, fetching task details, creating tasks, or closing tasks in ClickUp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmaggiezhou](https://clawhub.ai/user/mmaggiezhou)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and agents use this skill to query ClickUp task status, count due work, inspect spaces and lists, review assignee workload, and create or close tasks in a configured ClickUp workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation includes API-token checking instructions that could expose CLICKUP_API_KEY in terminal output or agent transcripts.

Mitigation: Use a dedicated least-privileged ClickUp token, avoid echoing the token, and prevent tokens from being logged in terminal or transcript output.

Risk: The helper supports state-changing ClickUp actions, including creating tasks and closing tasks in a live workspace.

Mitigation: Require explicit user approval before running create-task or close-task, and confirm the target list, task ID, title, assignee, and due date before execution.

Risk: Task queries may return workspace task descriptions, assignee information, task URLs, and other sensitive work data.

Mitigation: Limit use to the intended ClickUp team or list, review returned task data before sharing it, and avoid storing sensitive task output unnecessarily.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mmaggiezhou/skills/personal-task-tracking)
- [Publisher profile](https://clawhub.ai/user/mmaggiezhou)
- [ClickUp API v2](https://api.clickup.com/api/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, jq, and configured ClickUp environment variables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
