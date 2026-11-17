## Description:

Routes TikTok Shop ERP fulfillment requests through the LinkFox developer proxy to retrieve authorized shops and order split attributes for fulfillment workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations agents use this skill to check TikTok Shop authorized shops and determine whether specific orders can or must be split before fulfillment. It depends on linkfox-tiktok-shop-auth for shop selection and token handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports broader TikTok Shop ERP proxy authority than the narrow split-attribute workflow suggests.

Mitigation: Use only in a controlled environment with a trusted LinkFox gateway configuration, a narrowly scoped API key, and explicit human approval for fulfillment_proxy.py.

Risk: Arbitrary paths, methods, or request bodies can grant broader TikTok Shop ERP authority than the named read-only flow.

Mitigation: Prefer the named get_order_split_attributes flow and avoid arbitrary proxy parameters unless broader ERP authority is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-tiktok-shop-fulfillment)
- [TikTok Shop ERP Fulfillment API Reference](references/api.md)
- [Get Authorized Shops](references/apis/get_authorized_shops.md)
- [Get Order Split Attributes](references/apis/get_order_split_attributes.md)
- [TikTok Partner Center: Get Authorized Shops](https://partner.tiktokshop.com/docv2/page/get-authorized-shops-202309)
- [TikTok Partner Center: Get Order Split Attributes](https://partner.tiktokshop.com/docv2/page/get-order-split-attributes-202309)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses with concise Markdown guidance and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LinkFox agent API key, an ERP openId from linkfox-tiktok-shop-auth, and order_ids for split-attribute checks.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
