## Description:

Manage an executive's schedule, inbox, and communications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or delegated executive-support agents use this skill to prepare daily agenda reports, meeting context, inbox triage, calendar scheduling, and concise email replies for an executive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send email from the user's workspace without clearly requiring approval first.

Mitigation: Require explicit user approval before any email is sent, and review the skill before installation in a real executive workspace.

Risk: The skill is intended to read Google Workspace data for executive-assistant workflows.

Mitigation: Use it only where the agent is authorized to access the executive's Google Workspace data.

## Reference(s):

- [Persona Exec Assistant on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/persona-exec-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or conversational text with Google Workspace command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws binary and the gws-gmail, gws-calendar, gws-drive, and gws-chat utility skills.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
