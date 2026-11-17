## Description:

Local A-share analysis with Markdown/JSON reports, optional Feishu notifications, and optional iFinD enhancement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etherstrings](https://clawhub.ai/user/etherstrings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run a local JusticePlutus A-share analysis job for one or more stock codes, producing local Markdown and JSON reports with optional iFinD enrichment and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local analysis pipeline can use configured LLM, market-data, enrichment, and notification credentials.

Mitigation: Review the environment variables and webhook settings before enabling enrichment or notification modes.

Risk: Notification mode can send generated reports to configured external channels.

Mitigation: Use report-only mode or omit --notify when results should remain local.

## Reference(s):

- [JusticePlutus Skill Overview](references/overview.md)
- [ClawHub skill page](https://clawhub.ai/etherstrings/skills/justice-plutus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local Markdown/JSON report file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local report artifacts under reports/YYYY-MM-DD/ and may optionally send notifications when configured and explicitly enabled.]

## Skill Version(s):

2.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
