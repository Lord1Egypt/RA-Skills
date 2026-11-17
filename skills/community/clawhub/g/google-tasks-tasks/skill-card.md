## Description:

Google Tasks API integration with managed OAuth for managing task lists, tasks, due dates, notes, and completion state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an OpenClaw agent to Google Tasks through ClawLink, then inspect task lists and create, update, complete, move, or delete tasks with confirmation for write actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawLink acts as a hosted intermediary for Google Tasks OAuth flows and credential custody.

Mitigation: Review the Google OAuth consent screen, grant only the Tasks access intended, and use the ClawLink verification and dashboard links before connecting the account.

Risk: Write and destructive operations can create, update, delete, or clear Google Tasks data.

Mitigation: Preview write operations and confirm the target task list, task, and intended effect before execution.

## Reference(s):

- [Google Tasks API Overview](https://developers.google.com/tasks/reference/rest)
- [Google Tasks Tasklists Reference](https://developers.google.com/tasks/reference/rest/v1/tasklists)
- [Google Tasks Tasks Reference](https://developers.google.com/tasks/reference/rest/v1/tasks)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Google Tasks Connection](https://claw-link.dev/dashboard?add=google-tasks)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/google-tasks-tasks)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown guidance with bash command examples and JSON tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Google Tasks account through ClawLink for live API operations.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
