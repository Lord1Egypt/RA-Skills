## Description:

Reminders that reach the user by email, WhatsApp, SMS or phone call, in the steps and timing they choose. Stops when they acknowledge. Use when the user asks to be reminded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aditya-a-g](https://clawhub.ai/user/aditya-a-g)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create, inspect, pause, and cancel NudgeBell reminders that notify the account owner through chosen channels such as email, WhatsApp, SMS, or phone call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the user's NudgeBell API key and sends reminder content to NudgeBell.

Mitigation: Install only when the user is comfortable granting NudgeBell account access through NUDGEBELL_API_KEY and sending reminder content to the service.

Risk: Phone, SMS, and WhatsApp reminder steps can consume NudgeBell account credits.

Mitigation: Review the exact reminder steps, channels, timing, and account balance before creating reminders.

Risk: Scheduled reminders continue on NudgeBell until acknowledged, paused, or cancelled.

Mitigation: Use status checks to verify delivery and pause or cancel reminders when the user asks to stop them.

Risk: Cancelling a reminder permanently deletes it and its history.

Mitigation: Prefer pausing unless the user explicitly asks to delete or stop the reminder for good.

## Reference(s):

- [NudgeBell ClawHub Skill Page](https://clawhub.ai/aditya-a-g/skills/nudgebell)
- [NudgeBell Homepage](https://nudgebell.app)
- [NudgeBell API Reference](https://nudgebell.app/llms-full.txt)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with curl commands, JSON payloads, and optional MCP configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NUDGEBELL_API_KEY. Reminder creation and delivery may consume NudgeBell account credits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
