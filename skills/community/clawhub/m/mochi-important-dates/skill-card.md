## Description:

Track Gregorian and lunar birthdays, anniversaries and sourced annual holidays, with advance alerts, time zones, leap-day policies and calendar export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and families use the skill to record birthdays, anniversaries, milestones, and sourced annual holidays; review upcoming dates, schedule reminders, and export dated events to a calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private date records and reminder settings could be exposed if workspace state or credentials are shared.

Mitigation: Keep the .mochilab data private and use the host's private account configuration for delivery.

Risk: Incorrect recipients, time zones, or schedules can send reminders to the wrong destination or at the wrong time; inactive scheduled jobs may continue running.

Mitigation: Verify recipients, time zones, and schedules, and disable scheduled jobs when they are no longer needed.

Risk: An export may replace an existing calendar file if its filename is reused.

Mitigation: Choose a fresh export filename.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-important-dates)
- [MochiLab](https://mochilab.bz)
- [JSON actions and event fields](artifact/references/input.md)
- [Host scheduling and delivery guidance](artifact/references/notifications.md)
- [OpenClaw scheduling guide](https://docs.openclaw.ai/automation/cron-jobs)

## Skill Output:

**Output Type(s):** [JSON, Calendar files, Notification messages]

**Output Format:** [JSON action receipts and iCalendar (.ics) exports; reminder messages delivered through the configured host]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Event data is stored in the agent workspace. Automated reminders require a configured host scheduler and delivery channel; ICS exports are snapshots rather than live subscriptions.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
