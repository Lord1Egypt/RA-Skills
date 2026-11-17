## Description:

Generates practical lifestyle guides by researching recommendations from social media and official sources, cross-validating findings to filter promotional content, and organizing results into concrete travel, sports, food, or shopping guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhs1r](https://clawhub.ai/user/zhs1r)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create practical, medium-length lifestyle guides for trips, outdoor activities, sports venues or equipment, local food, and shopping. It is intended to gather current recommendations, compare them against official information, surface negative feedback, and produce a ready-to-use Markdown guide.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce outdated or incorrect practical advice for prices, opening hours, transport, policies, or seasonal conditions.

Mitigation: Use official or recent sources for time-sensitive facts, include an information-as-of date, and tell readers to confirm final prices and availability with official sources.

Risk: The skill may rely on promotional social media posts or single-source recommendations.

Mitigation: Require cross-verification across independent sources, preserve negative feedback in an avoid-list section, and label weakly supported recommendations.

Risk: The skill may request local retrieval commands for article content.

Mitigation: Run local commands only when the exact URL and command are visible and approved, and avoid PowerShell or curl retrieval when that approval is not available.

## Reference(s):

- [Output Template Library](references/output_templates.md)
- [ClawHub Skill Page](https://clawhub.ai/zhs1r/skills/guide-generator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guide with tables, source notes, practical itinerary or recommendation sections, and date-of-validity notice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask clarifying questions before drafting and may offer to save the resulting guide as a local Markdown file.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
