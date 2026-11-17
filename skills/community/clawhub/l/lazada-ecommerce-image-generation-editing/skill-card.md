## Description:

Create and edit Lazada product catalog images, SKU galleries, specification graphics, campaign tiles and localized storefront visuals. Use this skill for Lazada商品图、东南亚电商主图、LazMall视觉、商品详情图、多语言图片、活动素材、批量SKU和换背景；supports product-reference accuracy and AI Hive generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External Lazada sellers, catalog teams, and ecommerce operators use this skill to generate or edit product-reference catalog images, SKU galleries, campaign backgrounds, localization bases, and variant matrices while preserving product facts and leaving commercial claims for approved copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if a custom or untrusted AI Hive-compatible endpoint is used.

Mitigation: Use a dedicated, revocable AI Hive API key and avoid custom base URLs unless the endpoint is controlled and trusted.

Risk: Generated task outputs may be downloaded from URLs with weak controls.

Mitigation: Use submit-only mode or a constrained output directory for untrusted tasks, and review downloaded files before use.

Risk: Generated ecommerce visuals may contain incorrect prices, ratings, badges, warranties, compliance claims, or localized text.

Mitigation: Keep commercial claims and translated copy out of generated pixels, add them from approved seller data after generation, and validate current marketplace rules before publication.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/lazada-ecommerce-image-generation-editing)
- [AI Hive API Base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API Access Page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Image files]

**Output Format:** [Markdown guidance with bash commands and JSON API/task responses; generated image files are downloaded as PNGs unless submit-only mode is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI_HIVE_API_KEY; supports reference images, batch size, model parameters, routing mode, output directory, and no-download mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
