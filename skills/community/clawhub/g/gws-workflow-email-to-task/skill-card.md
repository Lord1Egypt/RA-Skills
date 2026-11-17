## Description:

Google Workflow: Convert a Gmail message into a Google Tasks entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents managing Google Workspace tasks use this skill to turn a specific Gmail message into a Google Tasks entry after confirming the message ID and target task list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads part of a Gmail message and creates a new Google Task.

Mitigation: Confirm the Gmail message ID and target task list with the user before running the workflow.

Risk: The workflow depends on the local gws Google Workspace tooling and its authenticated access.

Mitigation: Install only in environments where the gws tooling is trusted and intended for use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-workflow-email-to-task)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and Google Workspace authentication; creates a Google Tasks entry from a Gmail message after user confirmation.]

## Skill Version(s):

1.0.12 (source: server release metadata); source skill metadata 0.22.5

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
