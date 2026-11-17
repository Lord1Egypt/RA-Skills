## Description:

Schedules Indonesian prayer-time reminders to OpenClaw System Event from a configured location, with daily Islamic quotes and automatic Ramadan status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zckyachmd](https://clawhub.ai/user/zckyachmd)

### License/Terms of Use:

BSD-3-Clause

## Use Case:

External users and developers use this skill to schedule same-day Indonesian prayer reminders in OpenClaw based on configured coordinates, calculation settings, and local timezone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured latitude and longitude are sent to the AlAdhan API to calculate prayer times.

Mitigation: Review configured coordinates before use and only run the skill when sharing that location data with the provider is acceptable.

Risk: OpenClaw system-event reminders are created from third-party API timing data that is not strictly validated.

Mitigation: Run dry-run first, inspect planned reminder times, and consider stricter time validation before normal scheduling.

Risk: Normal execution creates OpenClaw one-shot cron entries.

Mitigation: Use dry-run during setup and restrict normal execution to trusted configurations and expected daily scheduling windows.

## Reference(s):

- [Prayer Times Id on ClawHub](https://clawhub.ai/zckyachmd/skills/prayer-times-id)
- [AlAdhan Timings API](https://api.aladhan.com/v1/timings)
- [AlAdhan Gregorian-to-Hijri API](https://api.aladhan.com/v1/gToH)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON execution summary with OpenClaw cron/system-event reminder registrations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mode reports planned jobs without registering cron entries; normal mode registers one-shot reminders for remaining prayer times on the current day.]

## Skill Version(s):

1.0.3 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
