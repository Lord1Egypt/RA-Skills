## Description:

用 AI Hive Nano Banana 2 把真实 SKU 参考图制作成可审核的电商主图，明确商品事实、必须保持项、允许变化、平台用途和安全留白，支持 Amazon、淘宝、天猫、京东、拼多多、抖音电商、小红书、TikTok Shop 与 Shopify。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce sellers, creative teams, and marketplace operators use this skill to generate reviewable product main-image candidates from authorized SKU reference photos while preserving product facts, required visual details, and platform-specific safe zones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote image service can influence downloaded output path behavior and download size.

Mitigation: Run the skill in an isolated environment, use --no-download for prompt checks, or download into a disposable output directory away from important writable files.

Risk: The workflow uploads product reference images to AI Hive and may store an API key locally.

Mitigation: Use only authorized product images, install only if the AI Hive service is trusted, and prefer environment-provided or replaceable API keys.

Risk: Generated marketplace images may still contain product-detail drift or text that does not meet current platform rules.

Mitigation: Compare outputs against reference images and manually verify dimensions, safe zones, text, prohibited claims, and marketplace rules before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-ecommerce-main-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print a prompt brief without upload, submit Nano Banana 2 image-generation tasks, poll task status, and optionally download PNG results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
