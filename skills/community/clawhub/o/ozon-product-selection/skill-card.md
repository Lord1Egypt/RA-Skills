## Description:

Helps agents identify Ozon product opportunities by researching category trends, deriving niche keywords, querying AlphaShop/1688 product search APIs, filtering offers, and presenting up to three recommended products with SKU details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, sourcing teams, and agent users use this skill to find candidate products for Ozon sales by combining market trend research with filtered AlphaShop/1688 supplier results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends product search terms and product IDs to AlphaShop and consumes AlphaShop API credits.

Mitigation: Confirm the category and filters before API use, especially for generic requests, and monitor AlphaShop credit usage.

Risk: The skill requires AlphaShop access and secret keys.

Mitigation: Store credentials as sensitive environment variables, avoid committing them, and rotate them if exposed.

Risk: Dependency versions are broad in the release evidence.

Mitigation: Pin reviewed dependency versions before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/ozon-product-selection)
- [1688aiinfra publisher profile](https://clawhub.ai/user/1688aiinfra)
- [AlphaShop API key management](https://www.alphashop.cn/seller-center/apikey-management)
- [AlphaShop API credits](https://www.alphashop.cn/seller-center/home/api-list)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown product recommendations with image links, product links, SKU tables, summaries, and JSON returned by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AlphaShop access and secret keys; may use web search and paid AlphaShop API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata, skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
