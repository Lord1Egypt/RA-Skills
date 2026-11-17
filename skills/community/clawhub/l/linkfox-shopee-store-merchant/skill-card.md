## Description:

Provides agent workflows and Python helpers for querying authorized Shopee cross-border merchant data, including merchant profile, shop lists, warehouses, warehouse locations, eligible shops, and prepaid accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers working with authorized Shopee cross-border merchant accounts use this skill to retrieve merchant, shop, warehouse, eligible-shop, and prepaid-account information through LinkFox-supported Shopee Merchant API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopee merchant/account data and LinkFox credentials may be sent through LinkFox services.

Mitigation: Install and run the skill only when that data path is acceptable for the user's merchant account and organization.

Risk: Phone numbers, SMS codes, API keys, merchant IDs, and saved response files may contain sensitive information.

Mitigation: Treat those values as secrets, avoid sharing logs or outputs that contain them, and remove or protect saved response files after use.

Risk: The skill includes onboarding and payment flows that can affect account setup or billing.

Mitigation: Review the onboarding and billing flow before allowing it to run, and require explicit user confirmation before registration, plan selection, or payment actions.

Risk: Environment overrides can change which LinkFox services receive requests.

Mitigation: Use trusted environment configuration and avoid running the skill with untrusted service endpoint overrides.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-merchant)
- [Shopee Merchant API reference](https://open.shopee.com/documents/v2/v2.merchant.get_merchant_info?module=93&type=1)
- [LinkFox merchant API reference](references/api.md)
- [Onboarding and billing reference](references/onboarding.md)
- [get_merchant_info reference](references/apis/get-merchant-info.md)
- [get_shop_list_by_merchant reference](references/apis/get-shop-list-by-merchant.md)
- [get_merchant_warehouse_list reference](references/apis/get-merchant-warehouse-list.md)
- [get_merchant_warehouse_location_list reference](references/apis/get-merchant-warehouse-location-list.md)
- [get_warehouse_eligible_shop_list reference](references/apis/get-warehouse-eligible-shop-list.md)
- [get_merchant_prepaid_account_list reference](references/apis/get-merchant-prepaid-account-list.md)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; API responses are JSON saved to local files and optionally printed to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large API responses are summarized on stdout unless inline output is requested; full responses are retained in a local linkfox output directory.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
