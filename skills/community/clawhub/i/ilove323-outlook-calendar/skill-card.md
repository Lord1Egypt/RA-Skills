## Description:

Reads Microsoft 365 Outlook calendar events for user requests about schedules, meetings, tasks, and date ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilove323](https://clawhub.ai/user/ilove323)

### License/Terms of Use:


## Use Case:

Employees and assistants use this skill to retrieve Outlook calendar events, summarize meetings, and calculate scheduled meeting time for today, tomorrow, a week, a month, or a custom date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Microsoft account credentials, cookies, and bearer tokens in files under ~/.outlook/.

Mitigation: Use only in an isolated, trusted environment, avoid storing a primary Microsoft password unless the account risk is accepted, and restrict file permissions for ~/.outlook/.

Risk: Calendar access relies on reusable session material and an intercepted Outlook Web bearer token rather than official scoped OAuth storage.

Mitigation: Prefer a version that uses official Microsoft OAuth with calendar-read-only scopes, secure token storage, and a clear cleanup or revocation path.

Risk: The activation language is broad and may run for many schedule, work, task, or meeting-related prompts.

Mitigation: Review and narrow activation rules before deployment so the skill runs only when calendar access is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilove323/skills/ilove323-outlook-calendar)
- [Publisher profile](https://clawhub.ai/user/ilove323)
- [Microsoft sign-in](https://login.microsoftonline.com)
- [Outlook calendar](https://outlook.office.com/calendar/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON calendar event output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar data may include event subjects, start and end times, duration, organizer, free/busy status, and all-day flags.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
