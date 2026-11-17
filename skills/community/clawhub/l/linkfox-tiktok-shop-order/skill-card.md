## Description:

Helps agents use LinkFox's TikTok Shop ERP order skill to retrieve authorized shops, search order lists, and fetch order details through documented TikTok Shop Order Open API paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to query TikTok Shop ERP order data, including authorized shops, filtered order lists, and order details. It is scoped to order lookup workflows and depends on the separate LinkFox TikTok Shop auth skill for seller authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway configuration can be overridden, which could send credentials or order data to an unintended destination.

Mitigation: Use only trusted HTTPS gateway settings and do not override LINKFOX_TOOL_GATEWAY or TIKTOK_SHOP_API_BASE_URL unless the destination is controlled.

Risk: The skill handles authenticated seller order data that can include sensitive customer and business information.

Mitigation: Restrict the LinkFox API key to the minimum seller and order scope, and redact buyer contact, address, payment, and identifier fields unless an authorized user specifically needs them.

Risk: The generic proxy script exposes broader authenticated proxy behavior than the narrow named order lookup scripts.

Mitigation: Prefer the documented named read-only order scripts and avoid using order_proxy.py beyond documented order reads without review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-shop-order)
- [TikTok Shop ERP Order API Reference](references/api.md)
- [Get Authorized Shops Reference](references/apis/get_authorized_shops.md)
- [Get Order List Reference](references/apis/get_order_list.md)
- [Get Order Detail Reference](references/apis/get_order_detail.md)
- [Get Order Detail 202309 Reference](references/apis/get_order_detail_202309.md)
- [TikTok Shop Get Order List](https://partner.tiktokshop.com/docv2/page/get-order-list-202309)
- [TikTok Shop Get Authorized Shops](https://partner.tiktokshop.com/docv2/page/get-authorized-shops-202309)
- [TikTok Shop Get Order Detail 202507](https://partner.tiktokshop.com/docv2/page/get-order-detail-202507)
- [TikTok Shop Get Order Detail 202309](https://partner.tiktokshop.com/docv2/page/get-order-detail-202309)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API-call responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs focus on TikTok Shop ERP order reads, including authorized-shop lookup, order search, and order detail retrieval; authorization, fulfillment, cancellation, refund, and creator-side order workflows are out of scope.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
