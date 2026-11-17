## Description:

Screens Chinese A-share stocks from natural-language criteria covering market activity, technical patterns, financials, and sectors using iWenCai data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

A-share investors and analysts use this skill to screen stocks with conversational filters and review matching market data from iWenCai. Screening results are not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-screening queries and an iWenCai API key are sent to an external provider.

Mitigation: Use only when the user intends to query iWenCai and is comfortable sharing their screening criteria and API key with that provider.

Risk: Market-data screening may be mistaken for personalized investment advice.

Mitigation: Label results as screening data, cite iWenCai as the source, and avoid personalized buy or sell recommendations.

Risk: Optional enrichment may send the user's request to additional search or finance tools.

Mitigation: Seek explicit user consent before invoking additional tools for enrichment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/chen6896qqwee/skills/hithink-astock-selector)
- [iWenCai stock screening](https://www.iwencai.com/unifiedwap/chat)
- [iWenCai SkillHub](https://www.iwencai.com/skillhub)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown stock-screening tables and plain-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies the final screening query and attributes results to iWenCai; results may be paginated.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
