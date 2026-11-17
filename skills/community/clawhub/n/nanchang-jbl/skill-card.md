## Description:

Chinese-language customer-service skill for a Nanchang Carpoly paint distributor, helping answer questions about products, recommendations, promotions, after-sales policy, construction services, and store navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubuq-sys](https://clawhub.ai/user/liubuq-sys)

### License/Terms of Use:

MIT-0

## Use Case:

External customers and retail service agents use this skill to handle Chinese-language paint and renovation inquiries for the Nanchang Carpoly distributor, including product guidance, pricing caveats, promotions, after-sales routing, construction-service explanations, and nearby store recommendations.

### Deployment Geography for Use:

China (Nanchang, Jiangxi)

## Known Risks and Mitigations:

Risk: The skill can respond to broad renovation or paint terms outside the intended distributor context.

Mitigation: Enable it only for the Nanchang Carpoly distributor use case and confirm user intent before giving store, product, or promotion guidance.

Risk: Prices, promotions, stock, and store details may become stale.

Mitigation: Use the packaged reference files for current details and tell users final pricing, availability, and activity terms are confirmed by the store.

Risk: Users may ask the assistant to perform refunds, after-sales actions, appointments, or service dispatch.

Mitigation: Keep responses informational and route operational requests to the listed store phone or in-store process.

Risk: Unpinned package installation can introduce supply-chain uncertainty.

Mitigation: Use a trusted ClawHub installation path or pinned installer version, especially when running from privileged environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liubuq-sys/skills/nanchang-jbl)
- [门店基础信息](references/business-info.md)
- [商品信息](references/services.md)
- [商品推荐逻辑](references/recommendations.md)
- [促销活动与会员权益](references/promotions.md)
- [售后处理与服务](references/after-sales.md)
- [到店引导与体验](references/experience.md)
- [施工/安装服务](references/construction.md)
- [企业文化与信任背书](references/brand.md)
- [渠道商门店信息（南昌及周边）](references/stores.md)
- [图片素材](references/images.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational Chinese Markdown responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should use the packaged reference files for product, price, promotion, store, construction, and after-sales details.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact metadata lists 1.0.9)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
