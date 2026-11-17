## Description:

Shopee-店铺FBS helps agents query Shopee Brazil FBS shop enrollment, invoice error, shop block, and SKU block status through LinkFox developer proxy scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators and their agents use this skill to inspect authorized Shopee Brazil FBS enrollment, invoice-error, shop-block, and SKU-block status data. It is intended for status checks and troubleshooting before taking follow-up operational actions.

### Deployment Geography for Use:

Brazil (Shopee Brazil FBS workflows)

## Known Risks and Mitigations:

Risk: The skill handles LinkFox account credentials and authorized Shopee shop data, and saved responses or printed API keys may contain sensitive information.

Mitigation: Install only if you trust LinkFox with this data, use a clean environment, and treat saved response files and printed keys as secrets.

Risk: The bundled onboarding helpers include phone/SMS registration, API-key generation, billing plan listing, and payment order flows.

Mitigation: Run onboarding, billing, or order commands only when intentionally registering, resolving account access, or buying credits.

Risk: Endpoint environment variables can influence where LinkFox gateway and login requests are sent.

Mitigation: Use official LinkFox endpoint variables only and review environment configuration before running the scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-fbs)
- [Shopee FBS API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [query_br_shop_enrollment_status](references/apis/query-br-shop-enrollment-status.md)
- [query_br_shop_invoice_error](references/apis/query-br-shop-invoice-error.md)
- [query_br_shop_block_status](references/apis/query-br-shop-block-status.md)
- [query_br_sku_block_status](references/apis/query-br-sku-block-status.md)
- [Shopee Open Platform FBS enrollment status](https://open.shopee.com/documents/v2/v2.fbs.query_br_shop_enrollment_status?module=126&type=1)
- [Shopee Open Platform FBS invoice error](https://open.shopee.com/documents/v2/v2.fbs.query_br_shop_invoice_error?module=126&type=1)
- [Shopee Open Platform FBS shop block status](https://open.shopee.com/documents/v2/v2.fbs.query_br_shop_block_status?module=126&type=1)
- [Shopee Open Platform FBS SKU block status](https://open.shopee.com/documents/v2/v2.fbs.query_br_sku_block_status?module=126&type=1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON files, Guidance]

**Output Format:** [Markdown guidance with shell commands and saved JSON response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists full API responses under a local linkfox session directory; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
