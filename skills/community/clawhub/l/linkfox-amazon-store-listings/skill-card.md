## Description:

亚马逊卖家 Listing 刊登与商品类型定义管理，用于查询、搜索、创建、更新、局部修改和删除卖家 Listing，检查 ASIN 刊登限制，并查询 product type 及其 JSON Schema 属性要求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and their agents use this skill to manage seller-owned Listings through LinkFox and Amazon SP-API workflows. It supports Listing lookup, search, patch, put, delete, restrictions checks, and product type schema discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify Amazon seller listings, including create, update, patch, and delete actions.

Mitigation: Require explicit human confirmation before patch, put, or delete operations, and verify sellerId, region, SKU, marketplaceIds, productType, and request body before execution.

Risk: The skill can assist with LinkFox account login, API-key generation, billing, and payment/order flows.

Mitigation: Run only in a trusted environment, keep API keys out of shared logs, and require explicit user approval before login, API-key, payment, or order steps.

Risk: Saved LinkFox response files may contain sensitive seller or listing data.

Mitigation: Review generated linkfox response files before sharing or committing them and apply local data handling controls for seller information.

Risk: Custom LinkFox endpoint environment variables can redirect requests to a different destination.

Mitigation: Do not set custom LinkFox endpoint variables unless the destination is controlled and trusted.

## Reference(s):

- [Amazon 店铺 Listings API 参考](artifact/references/api.md)
- [解决认证和算力问题](artifact/references/onboarding.md)
- [getListingsItem](https://developer-docs.amazon.com/sp-api/reference/getlistingsitem)
- [searchListingsItems](https://developer-docs.amazon.com/sp-api/reference/searchlistingsitems)
- [patchListingsItem](https://developer-docs.amazon.com/sp-api/reference/patchlistingsitem)
- [putListingsItem](https://developer-docs.amazon.com/sp-api/reference/putlistingsitem)
- [deleteListingsItem](https://developer-docs.amazon.com/sp-api/reference/deletelistingsitem)
- [getListingsRestrictions](https://developer-docs.amazon.com/sp-api/reference/getlistingsrestrictions)
- [searchDefinitionsProductTypes](https://developer-docs.amazon.com/sp-api/reference/searchdefinitionsproducttypes)
- [getDefinitionsProductType](https://developer-docs.amazon.com/sp-api/reference/getdefinitionsproducttype)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-store-listings)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and JSON API responses; scripts save full JSON response files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include Amazon seller Listing data and LinkFox account or billing guidance.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
