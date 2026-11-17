## Description:

Handle HR workflows — onboarding, announcements, and employee comms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and HR operators use this skill to coordinate onboarding, announcements, employee communications, and related Google Workspace actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HR workflows can expose employee PII through calendar events, shared folders, chat announcements, or bulk email.

Mitigation: Review recipients, shared folders, calendar targets, and message content before sending or uploading, and use the skill's PII sanitization guidance for sensitive operations.

Risk: Google Workspace actions may send communications or upload files to the wrong audience if targets are incorrect.

Mitigation: Confirm Google Workspace command targets, especially for bulk announcements and onboarding document sharing, before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/googleworkspace-bot/skills/persona-hr-coordinator)
- [Publisher Profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Google Workspace shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command and the gws-gmail, gws-calendar, gws-drive, and gws-chat skills.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
