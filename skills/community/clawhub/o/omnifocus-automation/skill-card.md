## Description:

Manage OmniFocus tasks, projects, folders, tags, due dates, recurrence, and task status via Omni Automation on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coyote-git](https://clawhub.ai/user/coyote-git)

### License/Terms of Use:


## Use Case:

Developers and OmniFocus users use this skill to let an agent query and update OmniFocus task data for GTD workflows, project tracking, due dates, tags, and recurring tasks. It is intended for macOS environments where OmniFocus 3 or 4 is installed and automation access is granted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and change OmniFocus task, project, folder, tag, due date, note, recurrence, and completion data.

Mitigation: Install and use it only when agent access to OmniFocus data is intended, and review task IDs and proposed changes before running modifying commands.

Risk: The delete command removes OmniFocus tasks and may permanently remove user data.

Mitigation: Require explicit confirmation before delete operations and ask the agent to show matching task IDs before destructive actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coyote-git/skills/omnifocus-automation)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [JSON command responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, OmniFocus 3 or 4, and local automation permission.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
