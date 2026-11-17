## Description:

Scans your Google Calendar for upcoming flights and writes a personalized circadian adjustment plan back to your calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chadholdorf](https://clawhub.ai/user/chadholdorf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw users use Jetlag Planner to detect upcoming flights in their primary Google Calendar and create circadian adjustment reminders for sleep timing, light exposure, melatonin timing, and arrival-day planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Google Calendar access and can read the primary calendar.

Mitigation: Use fresh Google OAuth credentials created specifically for this skill and revoke the authorization when the skill is no longer needed.

Risk: The skill can automatically add many calendar events.

Mitigation: Run it manually first, review the events it creates, and remove or adjust unwanted entries before relying on recurring use.

Risk: Credential setup and saved OAuth tokens can expose sensitive access if mishandled.

Mitigation: Do not ask another bot to print secrets, keep .env and .oauth-token.json private, and restrict token file permissions.

## Reference(s):

- [Jetlag Planner on ClawHub](https://clawhub.ai/chadholdorf/skills/openclaw-jetlag)
- [Node.js](https://nodejs.org)
- [Google Cloud Console](https://console.cloud.google.com)
- [Google Calendar OAuth Scope](https://www.googleapis.com/auth/calendar)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text summary with setup guidance or execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create multiple Google Calendar events after OAuth authorization.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
