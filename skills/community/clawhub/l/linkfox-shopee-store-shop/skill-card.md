## Description:

Provides agent guidance and Python script entry points for Shopee Open Platform Shop APIs, including shop information, profile updates, warehouses, notifications, authorised reseller brands, Brazil onboarding status, and holiday mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query and manage authorized Shopee store settings through LinkFox gateway-backed scripts. It supports store profile inspection and updates, warehouse and notification checks, authorised reseller brand lookup, Brazil onboarding review, and holiday mode changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags login, billing, silent feedback, and sensitive local-storage behavior that requires review before use.

Mitigation: Install and run the skill only in a trusted environment, review account and billing flows before use, and inspect or delete saved response files that may contain shop, address, or KYC data.

Risk: Some scripts can change live store state, including profile fields and holiday mode.

Mitigation: Require explicit user confirmation before running write operations such as profile updates or holiday mode changes.

Risk: Endpoint override environment variables can redirect gateway traffic.

Mitigation: Run with no endpoint override variables set unless the user intentionally needs a reviewed alternate endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-shop)
- [Shopee Shop API overview](https://open.shopee.com/documents/v2/v2.shop.get_shop_info?module=92&type=1)
- [API parameter and field reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [get_shop_info API reference](references/apis/get-shop-info.md)
- [update_profile API reference](references/apis/update-profile.md)
- [set_shop_holiday_mode API reference](references/apis/set-shop-holiday-mode.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts require LinkFox API-key configuration and write full API responses under a local linkfox session directory while printing either full JSON or a summary.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
