## Description:

Ethnographic UX research skill that passively observes OpenClaw usage, extracts interaction data, detects friction and delight signals, and generates structured daily research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giulianomorse](https://clawhub.ai/user/giulianomorse)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users, developers, and UX/product teams use this skill to analyze local session transcripts, redact sensitive text, detect friction and delight patterns, and generate daily Markdown research reports and trend summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw conversation transcripts and writes derived session data, reports, quotes, behavioral summaries, and trend files on disk.

Mitigation: Install only for histories the user is comfortable analyzing, keep generated files local, and review or delete files in the skill's data and reports directories as needed.

Risk: The security review reports incomplete redaction and date-scoping safeguards.

Mitigation: Avoid running it on histories that may contain secrets or sensitive personal data until those issues are fixed, and review generated output before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/giulianomorse/skills/nutcrackertest)
- [UXR Observer Homepage](https://clawhub.com/skills/uxr-observer)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON analysis data, and concise text responses with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write redacted session JSON, trend JSON, and Markdown report files to local data and reports directories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
