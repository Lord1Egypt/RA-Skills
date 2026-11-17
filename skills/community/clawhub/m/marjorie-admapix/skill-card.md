## Description:

AdMapix helps agents search ad creatives, analyze apps, review rankings, track estimated downloads and revenue, and generate market insights through the AdMapix API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, growth analysts, and app developers use this skill to investigate ad creatives, app performance, rankings, audience distribution, estimated downloads and revenue, and market trends. It supports English and Chinese analysis workflows backed by AdMapix API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends ad intelligence queries and targets to the third-party AdMapix API using the configured API key.

Mitigation: Use it only where sharing those queries is acceptable, protect the API key, and avoid private or confidential business data unless that sharing has been approved.

Risk: Install guidance uses a broad package command rather than a pinned or organization-approved installer.

Mitigation: Prefer a pinned version or an organization-approved installation path before deploying the skill in managed environments.

Risk: Download and revenue outputs are third-party estimates and may be mistaken for official app metrics.

Mitigation: Label those figures as estimates in user-facing summaries and avoid using them as the sole basis for high-stakes decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marjoriebroad/skills/marjorie-admapix)
- [AdMapix Website](https://www.admapix.com)
- [SkillBoss Setup Guide](https://skillboss.co/skill.md)
- [Project Repository](https://github.com/fly0pants/admapix)
- [Creative Search API](references/api-creative.md)
- [Product & Company API](references/api-product.md)
- [Ranking API](references/api-ranking.md)
- [Download & Revenue API](references/api-download-revenue.md)
- [App Distribution API](references/api-distribution.md)
- [Market Analysis API](references/api-market.md)
- [Parameter Mapping Reference](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with tables, summaries, links, and inline shell commands or API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include H5 result links; requires SKILLBOSS_API_KEY; download and revenue figures are third-party estimates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
