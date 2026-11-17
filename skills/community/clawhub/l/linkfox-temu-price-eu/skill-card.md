## Description:

This skill helps agents manage Temu Europe product pricing through LinkFox gateway scripts for price order queries, SKU base-price changes, and recommended or estimated base prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, operators, and developer agents use this skill to query Temu EU pricing records, estimate recommended or base prices, and prepare SKU base-price updates through LinkFox-mediated Temu Partner EU APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle LinkFox and Temu credentials and may store Temu access tokens locally.

Mitigation: Use least-privilege Temu tokens, avoid or lock down the local token store on shared machines, and review credential handling before installation.

Risk: The skill includes scripts that can submit merchant SKU base-price changes.

Mitigation: Require human review of goods IDs, SKU IDs, currencies, and new prices before running change scripts, then query pricing records afterward to verify the result.

Risk: Generic proxy and file-download scripts broaden the skill beyond narrowly scoped pricing operations.

Mitigation: Prefer the EU-specific pricing scripts, use generic proxy or downloader scripts only when necessary, and keep gateway endpoint environment variables pointed only at trusted LinkFox hosts.

Risk: API responses may be written to local JSON files and can contain merchant or pricing data.

Mitigation: Restrict workspace access, review retained response files, and remove sensitive local artifacts when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-temu-price-eu)
- [linkfox-temu-price-eu API reference](references/api.md)
- [Temu accessToken authorization and retrieval](references/access-token.md)
- [Partner EU Price API catalog](references/partner-eu-catalog.md)
- [Price API documentation index](references/apis/README.md)
- [Price order query API](references/apis/bg-local-goods-priceorder-query.md)
- [SKU base-price change API](references/apis/bg-local-goods-priceorder-change-sku-price.md)
- [Base-price recommendation API](references/apis/temu-local-goods-baseprice-recommend.md)
- [Recommended price query API](references/apis/temu-local-goods-recommendedprice-query.md)
- [Temu Partner EU documentation](https://partner-eu.temu.com/documentation?menu_code=dfff38c23adf498d8a7cd55052bd3648)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON request or response artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may write full API responses to local JSON files and print either full responses or summaries depending on response size.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
