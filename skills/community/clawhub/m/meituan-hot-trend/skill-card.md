## Description:

Helps agents retrieve and summarize public Meituan merchant and offer information for lightweight comparison of ratings, prices, reviews, and promotions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to collect and summarize public Meituan merchant, product, and promotion details for internal analysis, alerts, and same-category comparisons.

### Deployment Geography for Use:

Global, subject to Meituan availability and local access rules.

## Known Risks and Mitigations:

Risk: Public Meituan prices, promotions, availability, and delivery details may be time-sensitive or region-sensitive.

Mitigation: Verify important details on Meituan at the time of use and include collection time, region, and source links in summaries.

Risk: The skill could be misused for ordering, account actions, private data access, bulk scraping, or bypassing platform controls.

Mitigation: Use it only for lightweight analysis of public pages; do not provide credentials, automate purchases, collect private data, scrape at scale, or bypass Meituan controls.

Risk: Dynamic page rendering and page layout changes can cause incomplete or incorrect extraction.

Mitigation: Prefer user-opened public pages, review extracted fields before acting on them, and treat missing or ambiguous fields as requiring manual confirmation.

## Reference(s):

- [Meituan homepage](https://www.meituan.com/)
- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/meituan-hot-trend)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries, comparison tables, and source-linked notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Price, availability, promotion, and distance details should include the collection time, region, and source link when available.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
