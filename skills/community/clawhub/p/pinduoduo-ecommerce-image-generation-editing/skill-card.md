## Description:

为拼多多店铺生成和编辑商品主图、SKU 套图、活动图、使用场景图和多多搜索/多多场景测图，支持参考图保真及 AI Hive 批量生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce merchants and operators use this skill to create and edit Pinduoduo product master images, SKU variants, specification images, activity images, usage scenes, and ad-test creatives while preserving product structure and keeping promotional claims for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be sent to a configurable endpoint.

Mitigation: Use the default AI Hive endpoint unless the custom AI_HIVE_BASE_URL is fully trusted, and treat ~/.ai-hive/config.json as a stored API credential.

Risk: The upload command can send arbitrary local files to the service.

Mitigation: Use explicit image paths and reserve standalone uploads for intended product media only.

Risk: Generated commerce images can introduce incorrect product details or promotional claims.

Mitigation: Validate each SKU against the source product, color and specification tables, and add prices, discounts, sales claims, and activity text only through reviewed post-processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/pinduoduo-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; helper output may include JSON task details and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive API credentials, can upload local reference images, and defaults downloads to ~/Downloads/AiHive.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
