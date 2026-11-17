## Description:

Delivers a daily 7 AM CDT briefing with local weather, one healthcare revenue cycle insight, Pittsburgh sports updates, and seasonal fantasy baseball news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3m2b](https://clawhub.ai/user/j3m2b)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to receive a concise morning briefing that combines local running weather, one healthcare revenue cycle insight, sports updates, and in-season fantasy baseball notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes an executable Gmail IMAP reader that is not disclosed in the skill instructions and can access sensitive inbox metadata.

Mitigation: Install only when Gmail IMAP access is intentionally needed; require explicit opt-in credentials, limit retrieval to needed headers, and disclose the email helper before use.

Risk: The email helper prints private sender and subject metadata in its briefing output.

Mitigation: Route output only to trusted channels and redact or minimize sender and subject details when sharing the brief.

## Reference(s):

- [Morning Brief on ClawHub](https://clawhub.ai/j3m2b/skills/jb-morning-brief)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands]

**Output Format:** [Markdown-style daily briefing with optional JSON cron configuration and console output from the email helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefing content is intended to stay under 300 words and lead with weather.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
