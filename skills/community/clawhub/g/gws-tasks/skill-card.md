## Description:

Google Tasks: Manage task lists and tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to inspect and propose Google Workspace CLI commands for managing authenticated Google Tasks task lists and tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to create, update, move, clear, or delete Google Tasks data through an authenticated gws setup.

Mitigation: Review generated gws commands before execution and confirm the target account, task list, task ID, and intended mutation.

Risk: Deleting task lists or assigned tasks can also delete assignment-linked items in Google Docs or Chat Spaces.

Mitigation: Require explicit confirmation before destructive task-list or assigned-task deletion, and prefer non-destructive inspection commands first.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated gws setup and command inspection before API method calls.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
