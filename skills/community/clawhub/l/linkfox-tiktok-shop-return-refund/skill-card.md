## Description:

Helps agents call LinkFox/TikTok Shop ERP return and refund APIs to retrieve valid reject reasons for return or cancellation requests through an authorized shop context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External agents assisting TikTok Shop sellers or support operators use this skill to fetch the allowed rejection reasons before refusing a return or cancellation. It requires the companion auth skill, an openId, and a valid return_or_cancel_id.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generic return_refund_proxy.py path can access broader seller API functionality than the main reject-reasons flow.

Mitigation: Route normal use through get_reject_reasons.py or return_refund_api.py with api=get_reject_reasons, and disable or avoid return_refund_proxy.py unless broader seller-API access has been approved.

Risk: Misconfigured LINKFOX_TOOL_GATEWAY or TIKTOK_SHOP_API_BASE_URL could send seller API requests to an untrusted endpoint.

Mitigation: Keep the default trusted gateway or set only reviewed HTTPS gateway URLs in the runtime environment.

Risk: The skill depends on seller authorization and shop context from linkfox-tiktok-shop-auth.

Mitigation: Install and verify the companion auth skill first, pass openId rather than raw tokens, and provide shop_cipher or shop_id when multiple shops are authorized.

## Reference(s):

- [TikTok Shop ERP Return & Refund API Reference](references/api.md)
- [Get Reject Reasons](references/apis/get_reject_reasons.md)
- [Get Authorized Shops](references/apis/get_authorized_shops.md)
- [TikTok Shop Partner Center: Get Reject Reasons](https://partner.tiktokshop.com/docv2/page/get-reject-reasons-202309)
- [TikTok Shop Partner Center: Get Authorized Shops](https://partner.tiktokshop.com/docv2/page/get-authorized-shops-202309)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LINKFOX_AGENT_API_KEY or LINKFOXAGENT_API_KEY and an openId resolved by linkfox-tiktok-shop-auth.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
