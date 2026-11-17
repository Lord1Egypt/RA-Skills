## Description:

Provides Islamic prayer times for worldwide locations using AlAdhan calculation methods and helps set up optional automated Salat reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diepox](https://clawhub.ai/user/diepox)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer prayer-time and next-prayer questions for a location, or to configure recurring reminders that fetch daily times and notify around each Salat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder setup may create recurring agent turns and background checks.

Mitigation: Enable automated reminders only after explicit user confirmation, and document how to disable or remove the jobs.

Risk: Setup guidance may recreate missing cron jobs without fresh confirmation.

Mitigation: Require user approval before creating, recreating, or modifying scheduled jobs.

Risk: Optional network workaround guidance includes privileged Cloudflare WARP commands.

Mitigation: Run privileged network changes only when an administrator has reviewed and approved them.

Risk: The artifact includes GitHub publishing guidance and a publishing script.

Mitigation: Ignore or remove publishing steps unless the user explicitly requests repository publication.

Risk: Prayer-time lookup sends location queries to the AlAdhan service.

Mitigation: Tell users that city, country, or coordinate inputs are sent to AlAdhan before enabling lookups or reminders.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diepox/skills/muslim-prayer-reminder)
- [Reminder setup guide](references/setup-reminders.md)
- [Prayer calculation methods](references/methods.md)
- [Example cron jobs](references/example-cron-jobs.json)
- [AlAdhan prayer times API](https://aladhan.com/prayer-times-api)
- [AlAdhan calculation methods endpoint](https://api.aladhan.com/v1/methods)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, JSON examples, and optional JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query the AlAdhan API and may propose recurring cron jobs when reminders are enabled.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
