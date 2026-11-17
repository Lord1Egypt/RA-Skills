## Description:

Searches and synthesizes official and community market information for products in specified regions, including prices, sales signals, reviews, trends, credibility ratings, descriptive tables, and analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyyfaith](https://clawhub.ai/user/zyyfaith)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to research the market for a product in a specific region, compare product-market signals across regions, and prepare evidence-grounded purchase or market analysis. It is suited for gathering pricing, sales indicators, reviews, channel availability, trends, and source credibility notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs external web searches and fetches pages, which can expose the agent to unreliable or untrusted web content.

Mitigation: Use the skill's source-tiering, credibility ratings, source links, and date checks to distinguish official, media, community, and uncertain information.

Risk: Market data can be incomplete, stale, or inconsistent across sources.

Mitigation: Prefer recent authoritative sources, label outdated or missing data, preserve source links, and explicitly note disagreements or gaps in the report.

Risk: The optional continuous tracking feature may create a recurring cron job.

Mitigation: Enable tracking only with user consent, limit tracking to high-credibility sources, and explain how to disable the recurring job before it is created.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zyyfaith/skills/product-market-research)
- [Credibility Guide](reference/credibility-guide.md)
- [Output Templates](reference/output-templates.md)
- [Search Strategies](reference/search-strategies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports with tables, source links, credibility ratings, and optional tracking setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include translated summaries, dated source notes, currency labels, uncertainty flags, and follow-up analysis options.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
