## Description:

Interact with Kanboard project management through JSON-RPC API calls for tasks, projects, boards, columns, swimlanes, comments, subtasks, and users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bivex](https://clawhub.ai/user/bivex)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to compose Kanboard JSON-RPC commands for board, project, task, user, permission, comment, subtask, tag, and workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make real Kanboard changes across projects, tasks, users, permissions, and deletion operations.

Mitigation: Use a least-privilege user API token where possible and manually confirm deletes, user changes, permission changes, and bulk operations before execution.

Risk: Kanboard credentials and API tokens are required for operation.

Mitigation: Require HTTPS for KANBOARD_URL, keep credentials in trusted environment variables, and avoid shared systems where process arguments are visible.

Risk: Bulk workflows can apply changes to many tasks at once.

Mitigation: List and review target project, task, user, or permission IDs before running loops or batch operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command templates and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, KANBOARD_URL, and Kanboard API credentials configured by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
