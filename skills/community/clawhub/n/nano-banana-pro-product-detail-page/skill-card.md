## Description:

This skill helps agents create a coherent scrolling product-detail visual narrative with Nano Banana Pro through AI Hive, covering hero, need, product reveal, proof, experience, and closing modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce designers, brand marketers, and agent operators use this skill to plan and generate consistent product-detail page image sequences for channels such as Taobao, Tmall, Amazon A+, Shopify, and similar PDP formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom AI Hive base URL can receive the bearer API key.

Mitigation: Use only the official AI Hive endpoint, avoid AI_HIVE_BASE_URL or --base-url values that point to third-party hosts, and prefer a dedicated API key that can be revoked.

Risk: Reference images uploaded for generation may contain sensitive product, brand, or personal material.

Mitigation: Inspect files before upload and avoid uploading confidential, unapproved, or privacy-sensitive assets.

Risk: Generated product-detail visuals may drift from approved product structure, materials, logos, prices, dimensions, or claims.

Mitigation: Run the continuity checks described by the skill and add prices, dimensions, regulated claims, and terms only through reviewed post-production copy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-product-detail-page)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash examples and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can submit image-generation tasks, upload reference images, poll task status, and download generated image files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
