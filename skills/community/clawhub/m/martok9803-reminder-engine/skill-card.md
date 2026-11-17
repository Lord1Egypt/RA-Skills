## Description:

Create, list, cancel, and snooze one-shot or recurring reminders using OpenClaw cron jobs with confirmation, timezone handling, and clear reminder text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martok9803](https://clawhub.ai/user/martok9803)

### License/Terms of Use:


## Use Case:

Agent users use this skill to convert natural-language reminder requests into confirmed one-shot or recurring cron jobs, and to list, cancel, or snooze existing reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminders may persist as cron jobs until they fire or are canceled.

Mitigation: Confirm the schedule before creation and periodically review or cancel recurring reminders that are no longer needed.

Risk: Reminder text can expose sensitive information when delivered later or in a public channel.

Mitigation: Avoid secrets in reminder payloads and warn before scheduling reminders for public channels.

Risk: Ambiguous dates or repeated schedules can create incorrect or spammy reminders.

Mitigation: Ask one clarifying question when timing is ambiguous and require explicit confirmation before creating recurring reminders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/martok9803/skills/martok9803-reminder-engine)
- [Publisher profile](https://clawhub.ai/user/martok9803)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with cron scheduling parameters and reminder management summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cron job schedules, reminder payload text, job identifiers, and next-run summaries.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
