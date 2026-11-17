## Description:

This skill helps agents retrieve TikTok Shop ERP logistics warehouse information through LinkFox, including authorized-shop lookup and warehouse-list retrieval for sales and return warehouses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, support teams, and developers use this skill to inspect TikTok Shop warehouse IDs, names, types, statuses, defaults, and address summaries before product listing or stock workflows. It relies on the separate LinkFox TikTok Shop auth skill for shop selection and does not handle order listing, fulfillment, or initial authorization setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use LinkFox and TikTok credentials through a broad developer proxy.

Mitigation: Install only for trusted publishers and environments where LinkFox gateway controls, credential access, and audit expectations are understood.

Risk: The artifact includes authorized-shop lookup even though authorization setup is outside the stated scope.

Mitigation: Use the separate auth skill for authorization and treat this skill's authorization endpoint use as shop-cipher discovery for logistics calls.

Risk: The gateway URL can be overridden by environment variables.

Mitigation: Keep gateway environment variables pinned to approved LinkFox endpoints and review environment configuration before running scripts.

Risk: Warehouse data can affect downstream listing and stock workflows if stale or copied to the wrong shop.

Mitigation: Confirm the selected openId, shop_cipher, warehouse_id, warehouse type, and effect status before using results in product or inventory changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-shop-logistics)
- [TikTok Shop Get Warehouse List](https://partner.tiktokshop.com/docv2/page/get-warehouse-list-202309)
- [TikTok Shop Get Authorized Shops](https://partner.tiktokshop.com/docv2/page/get-authorized-shops-202309)
- [API Reference](artifact/references/api.md)
- [Get Warehouse List Reference](artifact/references/apis/get_warehouse_list.md)
- [Get Authorized Shops Reference](artifact/references/apis/get_authorized_shops.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call LinkFox gateway scripts that return JSON from TikTok Shop logistics and authorization endpoints.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
