## Description:

Fetch Gmail emails from the last 24h, rank by importance, summarize into bullet points, and auto-create Google Calendar events for detected meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russidan-nadee](https://clawhub.ai/user/russidan-nadee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent fetch recent Gmail messages, summarize important email content, and create Google Calendar events for detected meetings or interviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to recent Gmail messages and permission to create Google Calendar events.

Mitigation: Install only after reviewing the requested OAuth scopes and use it only with accounts where this access is acceptable.

Risk: OAuth client secrets, callback URLs, and token.json can expose account access if mishandled.

Mitigation: Use a local OAuth flow when possible, avoid sharing secrets through chat, protect token.json, and revoke the token when access is no longer needed.

Risk: Calendar events may be created from email-derived content that is incomplete or misinterpreted.

Mitigation: Require a user-visible review step before creating events and confirm event title, date, time, and duration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/russidan-nadee/skills/gmail-daily-briefing)
- [Publisher Profile](https://clawhub.ai/user/russidan-nadee)
- [OpenClaw](https://openclaw.ai/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Gmail API Read-Only OAuth Scope](https://www.googleapis.com/auth/gmail.readonly)
- [Google Calendar Events OAuth Scope](https://www.googleapis.com/auth/calendar.events)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown summary with inline command execution results and calendar event status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, local OAuth credentials, token.json, Gmail read-only access, and Google Calendar event creation permission.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
