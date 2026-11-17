## Description:

Generates professional product images for e-commerce platforms (Amazon, Shopify, eBay, etc.). Supports 8 visual styles and 6 scene types optimized for different product categories. Use when user mentions "商品图", "product images", "Amazon listing", "电商图片", or needs e-commerce product photography.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boyd4y](https://clawhub.ai/user/boyd4y)

### License/Terms of Use:


## Use Case:

External sellers, e-commerce operators, and content creators use this skill to plan and generate product image sets tailored to marketplace requirements, visual style, and scene type. It guides product analysis, outline selection, prompt creation, image generation, and completion reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates planning files, prompts, generated images, and preference files in the user's workspace.

Mitigation: Review the first-time preferences before saving them and inspect generated session outputs before reuse or publication.

Risk: Product descriptions and reference images may include sensitive product, brand, or campaign material.

Mitigation: Provide only product details and reference images that are appropriate to use for image generation.

Risk: Generated marketplace imagery may need review for accuracy and platform compliance before publication.

Mitigation: Use the skill's confirmation checkpoints and platform requirement references to review image plans before generation and publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/boyd4y/skills/product-image-generator)
- [README](README.md)
- [Quick Start Guide](QUICKSTART.md)
- [Scene Guide](references/elements/scene-guide.md)
- [Amazon Platform Requirements](references/platforms/amazon.md)
- [Shopify Store Image Requirements](references/platforms/shopify.md)
- [eBay Platform Requirements](references/platforms/ebay.md)
- [Etsy Platform Requirements](references/platforms/etsy.md)
- [Taobao Platform Requirements](references/platforms/taobao.md)
- [JD.com Platform Requirements](references/platforms/jd.md)
- [Pinduoduo Platform Requirements](references/platforms/pinduoduo.md)
- [Product Analysis Framework](references/workflows/analysis-framework.md)
- [Outline Template](references/workflows/outline-template.md)
- [Prompt Assembly Guide](references/workflows/prompt-assembly.md)
- [Reference Image Guide](references/workflows/reference-guide.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Watermark Guide](references/config/watermark-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, image files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, saved planning files, generated image files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a product-specific session directory with source inputs, analysis, outline variants, a selected outline, prompts, and generated images.]

## Skill Version(s):

1.0.0 (source: skill frontmatter metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
