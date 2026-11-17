## Description:

Guides agents in creating, querying, updating, deleting, and organizing Feishu tasks and task lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenfa188](https://clawhub.ai/user/chenfa188)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams using Feishu use this skill to have an agent manage tasks, task lists, assignments, followers, due dates, completion state, and list membership.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The activation wording is broad and the skill can guide create, update, delete, completion, and membership actions for Feishu task data.

Mitigation: Users should be explicit when requesting task changes and review any write, completion, deletion, or membership action before it is sent to Feishu.

Risk: A task creator may lose edit access if they create a task without including themselves as a member.

Mitigation: When creating tasks, include the current user's Feishu open_id as current_user_id so the tool can add them as a follower.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenfa188/skills/openclaw-feishu-task)
- [Publisher profile](https://clawhub.ai/user/chenfa188)

## Skill Output:

**Output Type(s):** [guidance, API Calls, JSON, configuration]

**Output Format:** [Markdown guidance with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for Feishu task and task-list actions; users should review write actions before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
