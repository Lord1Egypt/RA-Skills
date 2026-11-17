## Description:

[Didoo AI] Analyzes Meta Ads campaign performance in depth: metrics, funnel, trends, and anomalies, producing structured analysis without recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elias-didoo](https://clawhub.ai/user/elias-didoo)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, growth operators, and agents use this skill to diagnose Meta Ads campaign performance, identify weak funnel points, trends, anomalies, and data caveats, and prepare structured analysis before any recommendation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Meta Marketing API access token and ad account ID to analyze account performance.

Mitigation: Use a read-only token limited to the ads_read scope and provide credentials only when Meta Ads analysis is intended.

Risk: Generic trigger words such as analyze or diagnose may activate the skill when a Meta Ads workflow was not intended.

Mitigation: Confirm the user wants Meta Ads campaign analysis before requesting credentials or making API calls.

## Reference(s):

- [Didoo AI Blog](https://didoo.ai/blog)
- [ClawHub Skill Page](https://clawhub.ai/elias-didoo/skills/meta-ads-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis only; stores campaign context, funnel weak points, trend signals, anomalies, data quality notes, and general landing-page diagnosis in session context.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
