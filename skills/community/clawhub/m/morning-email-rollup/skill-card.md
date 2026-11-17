## Description:

Daily morning rollup of important emails and calendar events at 8am with AI-generated summaries

This skill is ready for commercial/non-commercial use.

## Publisher:

[am-will](https://clawhub.ai/user/am-will)

### License/Terms of Use:


## Use Case:

Individuals and teams use this skill to receive a daily Markdown-formatted digest of selected Gmail messages and today's Google Calendar events, with email summaries generated through Gemini.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads recent important or starred Gmail messages and today's Google Calendar events.

Mitigation: Install only for accounts where this access is acceptable, and narrow the Gmail query if the default selection is too broad.

Risk: Selected email body content is sent to Gemini for summarization.

Mitigation: Avoid using the skill for sensitive mail, or disable Gemini summarization and rely on the local fallback behavior.

Risk: A daily cron schedule can repeatedly access and summarize email and calendar data.

Mitigation: Review the cron command before enabling it and disable or update the schedule when the rollup is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/am-will/skills/morning-email-rollup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-formatted text with setup and scheduling command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rollup size is controlled by MAX_EMAILS; each selected email body is truncated before Gemini summarization.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
