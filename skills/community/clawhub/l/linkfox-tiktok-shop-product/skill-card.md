## Description:

TikTok官方-店铺商品 helps agents manage TikTok Shop ERP products through LinkFox's TikTok Product Open API workflow, including prerequisite checks, shop cipher lookup, category and brand lookup, product search, create and edit actions, listing checks, activation, deactivation, price and inventory updates, deletion, and recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to inspect and change TikTok Shop ERP product catalogs after completing the separate LinkFox TikTok Shop authorization flow. It is intended for workflows such as listing readiness checks, catalog search, product creation or edits, activation, deactivation, price updates, inventory updates, deletion, and recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live TikTok Shop catalog changes such as product creation, edits, activation, deactivation, price changes, inventory changes, deletion, and recovery.

Mitigation: Confirm product IDs, SKU IDs, shop context, listing platforms, prices, inventory quantities, and request bodies before running mutating commands.

Risk: Gateway environment overrides could send requests through an untrusted endpoint.

Mitigation: Use trusted LinkFox gateway configuration and avoid untrusted LINKFOX_TOOL_GATEWAY or TIKTOK_SHOP_API_BASE_URL values.

Risk: Command output may include shop cipher values and business data.

Mitigation: Treat outputs as sensitive and avoid sharing full shop cipher, catalog, price, inventory, or order-adjacent business details unnecessarily.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-shop-product)
- [LinkFox Product API overview](references/api.md)
- [TikTok Shop Get Authorized Shops API](https://partner.tiktokshop.com/docv2/page/get-authorized-shops-202309)
- [TikTok Shop Check Listing Prerequisites API](https://partner.tiktokshop.com/docv2/page/check-listing-prerequisites-202312)
- [TikTok Shop Search Products API](https://partner.tiktokshop.com/docv2/page/search-products-202502)
- [TikTok Shop Create Product API](https://partner.tiktokshop.com/docv2/page/create-product-202309)
- [TikTok Shop Edit Product API](https://partner.tiktokshop.com/docv2/page/edit-product-202309)
- [TikTok Shop Update Price API](https://partner.tiktokshop.com/docv2/page/update-price-202309)
- [TikTok Shop Update Inventory API](https://partner.tiktokshop.com/docv2/page/update-inventory-202309)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return TikTok Shop product, shop, price, inventory, listing, and gateway response data.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
