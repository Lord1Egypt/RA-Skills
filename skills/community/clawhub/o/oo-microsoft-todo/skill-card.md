## Description:

Microsoft To Do (to-do.office.com). Use this skill for ANY Microsoft To Do request — reading, creating, updating, and deleting data. Whenever a task involves Microsoft To Do, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Microsoft To Do can ask the agent to read task lists and tasks, create or update items, and delete data through their connected account. The skill requires confirmation before writes and explicit approval before destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute changing third-party code and synchronize additional agent skills without separate approval; OOMOL mediates access to task data.

Mitigation: Review the setup path, use a separately reviewed and verified CLI release, decide whether to allow skill synchronization, and retain confirmation requirements for changes and deletion.

## Reference(s):

- [Microsoft To Do](https://to-do.office.com)
- [Microsoft Graph To Do API overview](https://learn.microsoft.com/graph/api/resources/todo-overview?view=graph-rest-1.0)
- [oo CLI project documentation used by the skill](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-microsoft-todo)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON inputs and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results are returned from Microsoft To Do; writes require confirmation and destructive actions require explicit approval.]

## Skill Version(s):

1.0.4 (source: metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
