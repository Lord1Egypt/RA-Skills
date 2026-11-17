## Description:

Market Intelligence Claw provides real-time strategic intelligence for ecommerce and digital businesses, covering competitors, market trends, pricing, keyword research, sentiment, brand monitoring, and related business decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhishekj9621](https://clawhub.ai/user/abhishekj9621)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and operators use this skill to plan approved market research and receive concise intelligence on competitors, pricing, search demand, trends, news, and customer sentiment. It supports ecommerce and digital-business decisions using free web search by default and optional paid data providers when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved searches can reveal market research interests to web search and third-party data providers.

Mitigation: Review each research plan before execution and keep confidential product codenames, private customer data, and sensitive business details out of external queries.

Risk: Optional paid providers can create unexpected cost exposure.

Mitigation: Use dedicated read-only credentials where available, set monthly spend caps, and approve paid calls only after reviewing the estimated cost.

Risk: Market data can be incomplete, estimated, or stale when a paid data source is unavailable.

Mitigation: Treat outputs as decision support, cite the source for each claim, and note when web search fallback was used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abhishekj9621/skills/market-intelligence-claw)
- [API setup guide](references/setup.md)
- [Competitor analysis module](references/competitor.md)
- [Trend analysis module](references/trends.md)
- [Keyword and SEO intelligence module](references/keywords-seo.md)
- [Pricing, news, and sentiment modules](references/modules-2.md)
- [SerpApi](https://serpapi.com)
- [Rainforest API](https://rainforestapi.com)
- [DataForSEO](https://dataforseo.com)
- [NewsAPI endpoint](https://newsapi.org/v2/everything)
- [Reddit API](https://reddit.com/dev/api)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, configuration, guidance]

**Output Format:** [Markdown reports, research plans, setup guidance, and concise strategic recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite the tools used for claims and note when data is estimated from web search fallback.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
