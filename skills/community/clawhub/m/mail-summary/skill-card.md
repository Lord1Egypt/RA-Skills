## Description:

Fetch Gmail emails from the last 24 hours, rank them by importance, summarize them into bullet points, and create Google Calendar events for detected meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[russidan-nadee](https://clawhub.ai/user/russidan-nadee)

### License/Terms of Use:

MIT-0

## Use Case:

Users and their agents use this skill to review recent Gmail messages, produce concise priority-ordered summaries, and add missing meeting or interview events to Google Calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Gmail read access and Google Calendar event-write access.

Mitigation: Use a Google account and OAuth consent configuration appropriate for the data being accessed, and revoke Google OAuth access when the skill is no longer needed.

Risk: Stored Google token files can grant continuing access if exposed.

Mitigation: Run the skill in a private environment and protect or delete stored credential and token files after use.

Risk: Email content may be printed in agent-visible output.

Mitigation: Avoid running the skill where logs or transcripts are shared with people who should not see private email content.

Risk: Automatically created Calendar events may be incorrect or unwanted.

Mitigation: Review proposed or newly created Calendar events and avoid unattended event creation for sensitive calendars.

Risk: The refresh service can maintain ongoing token access with limited user control.

Mitigation: Enable the refresh service only when needed for long-running or scheduled use, and stop it when the workflow is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/russidan-nadee/skills/mail-summary)
- [Publisher profile](https://clawhub.ai/user/russidan-nadee)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Agent instructions](artifact/agent/instructions.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style email summaries with sender, subject, bullet points, and optional Calendar event creation notices.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce Google OAuth authorization URLs, setup guidance, and Calendar event creation side effects.]

## Skill Version(s):

1.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
