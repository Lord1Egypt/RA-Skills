## Description:

Industry hotspot and competitor monitoring across 5 dimensions for Chinese-language requests with competitor URLs, using international English sources to produce a structured Chinese daily brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[law52525](https://clawhub.ai/user/law52525)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market intelligence teams use this skill to monitor industry trends and competitor activity from international English-language sources, then receive a Chinese daily brief with alerts and role-based action recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided search terms and competitor URLs are used in Bash-based browser commands without explicit validation.

Mitigation: Review before installation and use only trusted public https competitor URLs; avoid internal, localhost, private-network, or unusual scheme URLs.

Risk: URL handling may be unsafe for broad use without additional controls.

Mitigation: Add explicit URL validation, percent-encoding, redirect checks, and safe non-shell argument passing before broad deployment.

## Reference(s):

- [Monitoring Rules](references/monitoring-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/law52525/skills/market-radar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese Markdown daily brief for Telegram, including alert summaries, competitor monitoring tables, trend analysis, and action recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public web research results and translates English-source findings into Chinese; OpenClaw handles Telegram message segmentation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
