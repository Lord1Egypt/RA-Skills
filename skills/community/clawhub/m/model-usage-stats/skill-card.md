## Description:

Generates model usage summaries, token counts, cost estimates, and consumption reports across current or historical OpenClaw sessions, with results formatted for Feishu message cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luxiang79](https://clawhub.ai/user/luxiang79)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to review model token usage, estimate costs, compare consumption by model or session, and prepare shareable usage reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Historical session usage statistics can expose session identifiers or sensitive usage patterns if collected too broadly or shared through Feishu without consent.

Mitigation: Require explicit session or time-range selection, retrieve metadata only where possible, redact session IDs, and ask for confirmation before sending Feishu messages.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports and Feishu message-card content with tables, summaries, and cost calculations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include token totals, cost estimates, session or model breakdowns, and exportable consumption reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
