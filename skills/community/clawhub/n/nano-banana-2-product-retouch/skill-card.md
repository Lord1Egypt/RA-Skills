## Description:

使用 Nano Banana 2 对商品目录照片进行一致化精修，在不改变 SKU 事实的前提下统一曝光、白平衡、边缘、阴影、材质与画布占比。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External catalog and ecommerce operators use this skill to retouch product photos consistently across SKUs while preserving factual product details such as color, structure, labels, logos, accessories, defects, and quantity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected product images and prompts are uploaded to AI Hive for editing.

Mitigation: Use only approved catalog assets, avoid sensitive or unreleased product imagery, and install the skill only if the AI Hive service is trusted for that content.

Risk: API-provided result metadata can influence local output paths when completed results are downloaded.

Mitigation: Use a dedicated non-sensitive output directory and review or patch output-path handling before processing sensitive catalog assets.

Risk: Generated retouching can accidentally change product facts or hide defects in a way that misleads customers.

Mitigation: Compare each result against the original SKU, approved samples, and the catalog tolerance table; reject outputs that alter labels, structure, color, quantity, accessories, or required defect disclosure.

Risk: The helper requires an AI Hive API key for execution.

Mitigation: Use a dedicated API key, prefer environment-based secret handling where possible, and keep any local key file restricted to the current user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-product-retouch)
- [AI Hive API endpoint used by the skill](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page referenced by the skill](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; generated image files or JSON task status from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one user-selected product image and an AI Hive API key; defaults to downloading completed images to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
