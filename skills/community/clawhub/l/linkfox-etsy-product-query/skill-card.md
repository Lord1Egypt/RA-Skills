## Description:

Etsy商品查询 helps agents filter Etsy listings by keyword or URL, price, sales, favorites, reviews, listing date, category, product type, and marketplace tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce analysts, and agents use this skill to search and compare Etsy products by commercial signals such as sales, price, favorites, reviews, category, listing age, and product tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox account onboarding, API keys, and paid billing flows.

Mitigation: Install and use it only when LinkFox is trusted, avoid exposing API keys in shared files or logs, and require explicit user confirmation before onboarding or payment commands.

Risk: Endpoint override environment variables can direct requests away from the default LinkFox services.

Mitigation: Use endpoint overrides only when the destination is controlled and expected.

Risk: Etsy product queries consume paid credits dynamically and larger result pages can increase cost.

Mitigation: Confirm page size and expected cost with the user before running large queries or pagination.

## Reference(s):

- [_ehunt_productQuery API reference](artifact/references/api.md)
- [Authentication and billing onboarding](artifact/references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-etsy-product-query)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON API parameters, stdout summaries, and saved JSON response files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results may be summarized when responses are large; full responses are saved as JSON files by the query script.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
