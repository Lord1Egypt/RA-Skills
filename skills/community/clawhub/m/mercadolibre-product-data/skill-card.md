## Description:

Helps agents retrieve Mercado Libre listings, product details, reviews, buyer questions, and category best sellers through Scavio for Mexico, Brazil, Argentina, and Colombia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research listings, compare prices and sellers, read reviews and questions, and identify category best sellers across supported Mercado Libre markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, item IDs, listing URLs, and the API key are sent to Scavio.

Mitigation: Use the integration only when this disclosure is acceptable; avoid confidential listing URLs and store the API key in an environment variable or secret store.

Risk: Pagination and repeated requests can consume API credits.

Mitigation: Limit pages and monitor remaining credits when running loops.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/mercadolibre-product-data)
- [Scavio Mercado Libre search documentation](https://scavio.dev/docs/mercadolibre-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data)
- [Scavio Mercado Libre product documentation](https://scavio.dev/docs/mercadolibre-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data)
- [Scavio Mercado Libre reviews documentation](https://scavio.dev/docs/mercadolibre-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data)
- [Scavio Mercado Libre questions documentation](https://scavio.dev/docs/mercadolibre-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data)
- [Scavio Mercado Libre best sellers documentation](https://scavio.dev/docs/mercadolibre-best-sellers?utm_source=agent-skills&utm_medium=skill&utm_campaign=mercadolibre-product-data)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, JSON]

**Output Format:** [Markdown instructions and examples; structured JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Country-specific prices; paginated search, reviews, and questions.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
