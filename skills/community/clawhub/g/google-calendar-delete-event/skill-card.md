## Description:

Atomic node skill to delete a Google Calendar event using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to delete a specific Google Calendar event through the gog CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete a Google Calendar event when an agent runs a destructive gog command without built-in confirmation or event verification.

Mitigation: Require the agent to identify the exact calendar and event, restate what will be deleted, and get explicit confirmation before running the command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/google-calendar-delete-event)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [Markdown instructions with an inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and Google Calendar access to be configured before use.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
