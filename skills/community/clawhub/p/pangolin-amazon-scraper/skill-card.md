## Description:

Scrapes Amazon product data through Pangolin APIs for ASIN lookups, keyword searches, bestseller and new-release checks, reviews, pricing, cross-region comparisons, category browsing, and seller research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyu020923](https://clawhub.ai/user/liuyu020923)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for Amazon product research through Pangolin, including product detail lookups, keyword searches, rankings, reviews, seller options, and region comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to handle Pangolin credentials and stores a reusable API key in a local plaintext file.

Mitigation: Use a dedicated, revocable Pangolin API key, avoid sharing passwords in chat, remove ~/.pangolin_api_key when finished, and rotate the key if exposure is possible.

Risk: Multi-page review, cross-region, or repeated scraping requests can consume Pangolin credits and return point-in-time marketplace data.

Mitigation: Confirm scope before larger runs, warn about review-page credit costs, and present scraped Amazon data as current only for the time of retrieval.

## Reference(s):

- [Pangolinfo Amazon Scraper on ClawHub](https://clawhub.ai/liuyu020923/skills/pangolin-amazon-scraper)
- [Pangolin](https://www.pangolinfo.com)
- [Amazon Scrape API Reference](references/amazon-api.md)
- [Output Schema Reference](references/output-schema.md)
- [Error Codes and Troubleshooting](references/error-codes.md)
- [Keyword Search Example](references/examples/keyword-search-example.json)
- [Product Detail Example](references/examples/product-detail-example.json)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Pangolin credentials; API calls may consume Pangolin credits.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
