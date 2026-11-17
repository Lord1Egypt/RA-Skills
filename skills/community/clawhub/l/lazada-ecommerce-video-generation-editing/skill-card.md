## Description:

Create and edit Lazada product listing videos, localized demonstrations, LazMall brand clips and campaign-ready seller assets. Use this skill for Lazada商品视频、东南亚电商视频、商品详情演示、多语言版本、LazMall内容、活动素材、开箱和跨市场本地化；supports generation, reference, editing and AI Hive delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace operators, and content teams use this skill to generate and edit Lazada product videos, localized listing demonstrations, LazMall brand clips, campaign bases, and package-content clarifications. It helps keep marketplace, language, SKU, package contents, approved claims, and caption-safe regions aligned before review and publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable API base URL can send the user's AI Hive API key and product media to an unintended or plaintext endpoint.

Mitigation: Use the official HTTPS AI Hive endpoint unless testing with isolated credentials, and do not set --base-url, AI_HIVE_BASE_URL, or config base_url to an untrusted or http:// endpoint.

Risk: Generated marketplace videos may contain unsupported product claims, prices, badges, voucher text, warranty language, or localized copy errors.

Mitigation: Review one market before batching, verify SKU, units, package contents, approved benefits, seller-approved copy, and current Lazada marketplace requirements before publishing.

Risk: The runtime depends on requests without a pinned version in the artifact instructions.

Mitigation: Install dependencies in a virtual environment and pin or review the requests package before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/lazada-ecommerce-video-generation-editing)
- [AI Hive access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown with inline bash commands and CLI-generated JSON task output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can submit AI Hive video generation, editing, reference, extension, upload, task polling, and download workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
