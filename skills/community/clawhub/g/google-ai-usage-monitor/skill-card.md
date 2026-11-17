## Description:

Monitor Google AI Studio (Gemini API) usage, rate limits, and quota consumption with automated alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to monitor Google AI Studio quota usage, rate limits, and consumption trends, then send scheduled alerts before limits are exhausted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled Discord reports may disclose Google AI Studio project usage and quota information to the configured channel.

Mitigation: Confirm the Discord channel, mention target, and message templates are appropriate before enabling scheduled delivery.

Risk: Monitoring the wrong Google account, browser profile, project ID, schedule, or timezone could produce misleading reports or alerts.

Mitigation: Verify the browser profile, project ID, daily schedule, and timezone during setup and before relying on automated alerts.

## Reference(s):

- [Google AI Studio Usage Dashboard](https://aistudio.google.com/usage)
- [Gemini API Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Gemini API Billing Documentation](https://ai.google.dev/gemini-api/docs/billing)
- [Cloud Monitoring for Gemini](https://firebase.google.com/docs/ai-logic/monitoring)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, alert message templates, browser automation commands, and cron configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scheduled Discord reporting guidance and threshold-based alert templates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
