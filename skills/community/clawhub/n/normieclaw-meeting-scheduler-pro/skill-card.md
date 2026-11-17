## Description:

Meeting Scheduler Pro helps an OpenClaw agent schedule meetings, manage availability, prepare briefs and agendas, and capture follow-up work using Google Calendar, optional Gmail context, web search, and local notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external-facing professionals use this skill to coordinate meetings, find available time, create calendar events, generate meeting preparation, and track follow-up tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request broad Calendar read/write access and may use Gmail content, web search, local notes, and cross-skill data during meeting preparation.

Mitigation: Review config/settings.json before use, grant only acceptable gog permissions, and disable email context or web search for sensitive meetings.

Risk: Meeting notes and follow-up files can persist locally with attendee names, decisions, discussion points, and action items.

Mitigation: Review and prune the configured meeting-notes directory periodically and adjust retention practices for sensitive work.

Risk: Meeting content processed by the configured AI provider may be subject to that provider's data handling terms.

Mitigation: Confirm the configured AI provider's retention and training policies before processing confidential calendar, email, or meeting-note content.

Risk: The server security verdict is suspicious because the release defaults to automated calendar, Gmail, web-search, local-note, and cross-skill data use.

Mitigation: Install only after reviewing the security summary, settings, and required permissions, and verify gog is sourced from a trusted OpenClaw distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-meeting-scheduler-pro)
- [Publisher profile](https://clawhub.ai/user/nollio)
- [README](artifact/README.md)
- [Security considerations](artifact/SECURITY.md)
- [Default settings](artifact/config/settings.json)
- [Dashboard manifest](artifact/dashboard-kit/manifest.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and conversational text with inline shell commands, JSON configuration, calendar-event details, agendas, prep briefs, and follow-up task drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Google Calendar events through gog, write local markdown notes, and draft email or task follow-ups after user confirmation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
