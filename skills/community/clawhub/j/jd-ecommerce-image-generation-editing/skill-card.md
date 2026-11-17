## Description:

为京东店铺生成和编辑商品主图、规格图、结构卖点图、场景图与京准通广告图片，并通过 AI Hive 支持参考图保真、批量方向生成和结果下载。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

京东商家、运营、广告投放人员和视觉设计人员使用该技能，为商品主图、结构卖点图、包装清单图、场景图和京准通广告测图生成可复核的图片制作指令与 AI Hive 调用命令。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and send an AI Hive API key and user media through configurable endpoints.

Mitigation: Use a dedicated low-privilege AI Hive API key, avoid custom base URLs unless trusted, upload only media appropriate for the configured service, and install dependencies in an isolated pinned environment.

Risk: Generated ecommerce imagery can introduce unsupported product specs, certifications, pricing, sales claims, accessories, or marketplace-rule issues.

Mitigation: Restrict prompts to merchant-provided facts, leave complex parameter text for manual layout, and review final assets against current category and advertising rules before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/jd-ecommerce-image-generation-editing)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact changelog](artifact/CHANGELOG.md)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash command examples and JSON configuration examples; the bundled script can download generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses reference images, batch size, routing, output directory, and download controls when supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
