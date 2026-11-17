## Description:

Privacy-first UX research ethnography for OpenClaw that observes local usage, analyzes workflow friction, and generates redacted daily reports with metrics, insights, recommendations, and next-day research plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giulianomorse](https://clawhub.ai/user/giulianomorse)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw teams use this skill to collect consented local session data, identify UX friction, and produce daily redacted ethnography reports for product, documentation, and workflow improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can repeatedly collect and store broad conversation history and operational logs when consent settings allow it.

Mitigation: Review consent settings before use, prefer this_session_only and minimal capture by default, and avoid recurring cron runs until recurring collection is explicitly acceptable.

Risk: Captured transcripts and reports may include sensitive content if broader capture levels are selected.

Mitigation: Apply the bundled redaction rules before writing files, redact uncertain sensitive content, and use purge or purge full when reports are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/giulianomorse/skills/nutcrackertestgpt)
- [Fallback Session Paths](artifact/references/fallback-session-paths.md)
- [Redaction Rules](artifact/references/redaction-rules.md)
- [Report Template](artifact/references/report-template.md)
- [Summary Schema](artifact/references/summary-schema.json)
- [Creating OpenClaw Skills](https://docs.openclaw.ai/tools/creating-skills)
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)
- [OpenClaw Skills Config](https://docs.openclaw.ai/tools/skills-config)
- [OpenClaw Cron Jobs](https://docs.openclaw.ai/tools/cron-jobs)
- [OpenClaw Session Management](https://docs.openclaw.ai/tools/session-management)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON summaries, local data files, and concise chat guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local-only and should be redacted according to the configured capture level, consent scope, and retention window.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
