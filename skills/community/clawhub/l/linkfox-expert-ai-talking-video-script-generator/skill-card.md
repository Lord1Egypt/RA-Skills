## Description:

为跨境电商产品生成 Seedance 2.5 导演级口播视频 Prompt。评论情绪故事挖掘、钩子策略映射、多变体生成、七关质检门控和品类知识沉淀，覆盖 ASIN、商品链接、产品图片和直接描述输入。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, creators, and advertising teams use this skill to turn product details, reviews, links, images, and direct descriptions into data-grounded talking-head video script prompts. It produces strategy decisions, multiple Seedance-ready prompt variants, quality checks, reference-binding advice, and material lists for cross-border product marketing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkFox services may receive product URLs, review data, prompts, images, API credentials, and task feedback.

Mitigation: Use the skill only with data approved for LinkFox processing, and avoid submitting private or sensitive product, customer, credential, or campaign information.

Risk: Credentialed LinkFox calls rely on gateway environment variables with under-scoped controls.

Mitigation: Pin gateway environment variables to trusted LinkFox HTTPS hosts and review credential handling before deployment.

Risk: Some workflow paths can upload local files or use public image URLs, which may expose material outside the local environment.

Mitigation: Do not upload private local files, and confirm that any file or image URL is appropriate for public or third-party access before use.

Risk: The skill may retain task-derived knowledge and submit some feedback without interrupting the user's flow.

Mitigation: Require explicit approval for memory retention and feedback submission before using those behaviors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-ai-talking-video-script-generator)
- [Seedance prompt structure](artifact/skills/seedance-product-oral-script/references/prompt-structure.md)
- [Seedance camera physics](artifact/skills/seedance-product-oral-script/references/camera-physics.md)
- [Seedance product binding](artifact/skills/seedance-product-oral-script/references/product-binding.md)
- [LinkFox Amazon product detail API](artifact/skills/linkfox-amazon-product-detail/references/api.md)
- [LinkFox Amazon reviews API](artifact/skills/linkfox-amazon-reviews-list/references/api.md)
- [LinkFox Amazon image search API](artifact/skills/linkfox-amazon-search-by-image/references/api.md)
- [LinkFox web data crawler API](artifact/skills/linkfox-plugin-web-data-crawler/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured strategy cards, Seedance prompt variants, quality reports, reference-binding guidance, material lists, and optional LinkFox suggestion tags.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are grounded in user-provided or LinkFox-returned product data; data collection paths may require LinkFox API credentials and publicly reachable image or file URLs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
