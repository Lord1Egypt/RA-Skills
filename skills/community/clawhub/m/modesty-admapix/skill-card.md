## Description:

Admapix helps agents search ad creatives, analyze apps, inspect rankings, track estimated downloads and revenue, and summarize market intelligence through the AdMapix API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing, growth, and app-intelligence users use this skill to search ad creatives, inspect app and developer activity, compare competitors, review rankings, and summarize estimated downloads, revenue, and market trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends app, market, and competitor-analysis queries to api.admapix.com using the user's API key.

Mitigation: Install only when AdMapix is trusted, keep the API key scoped and private, and avoid confidential prompts.

Risk: Estimated download and revenue data could be mistaken for official app-store or publisher data.

Mitigation: Preserve the skill's third-party-estimate disclaimer whenever download or revenue figures are presented.

Risk: Unversioned installer commands may resolve to a later release than the one reviewed.

Mitigation: Prefer a pinned or verified ClawHub installer command for deployment.

Risk: API permissions, rate limits, upstream errors, or empty results can make multi-step analysis partial.

Mitigation: Report unavailable data clearly, retry transient upstream failures once, and complete only the supported parts of the analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/skills/modesty-admapix)
- [AdMapix Website](https://www.admapix.com)
- [Creative Search API](references/api-creative.md)
- [Product & Company API](references/api-product.md)
- [Ranking API](references/api-ranking.md)
- [Download & Revenue API](references/api-download-revenue.md)
- [App Distribution API](references/api-distribution.md)
- [Market Analysis API](references/api-market.md)
- [Parameter Mapping Reference](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, tables, comparisons, H5 result links, setup guidance, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English/Chinese output; download and revenue figures are presented as third-party estimates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
