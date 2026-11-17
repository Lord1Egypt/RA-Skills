## Description:

Helps agents research H&M products, categories, availability, reviews, and nearby stores through Crawlora's catalog API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and shopping assistants use this skill to browse or search H&M products, compare product details and stock, and find nearby stores without scraping H&M pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Catalog and store queries are sent through Crawlora, a third-party intermediary.

Mitigation: Use only if this intermediary is acceptable for the task; avoid including unnecessary sensitive personal details in search or store-location queries.

Risk: Exposing the Crawlora API key could allow unauthorized use.

Mitigation: Keep CRAWLORA_API_KEY secret in the environment; never include it in prompts, query parameters, or committed files.

## Reference(s):

- [ClawHub hm-research release](https://clawhub.ai/crawlora-org/skills/hm-research)
- [H&M endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown responses informed by JSON product and store data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Catalog listings and searches are paginated; detailed size availability and reviews require a product-detail lookup.]

## Skill Version(s):

1.0.16 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
