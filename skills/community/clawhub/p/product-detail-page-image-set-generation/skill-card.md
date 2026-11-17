## Description:

使用 Nano Banana Pro 把商品资料转换成完整详情页套图镜头清单，并逐模块生成首屏、利益、结构、步骤、尺寸、场景和装箱图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, product marketers, and designers use this skill to turn approved product facts and reference images into a module-by-module product detail page image set. It helps generate visual bases for hero, benefit, structure, usage, sizing, scene, package, and limitation modules while preserving product evidence for later human layout and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated task data can direct downloads in ways that may overwrite files or consume unbounded storage.

Mitigation: Run in an isolated environment, choose a non-sensitive output directory, and add URL validation, file size limits, and output-path containment before broader use.

Risk: The skill stores an API key locally and uploads selected product reference images to AI Hive.

Mitigation: Install only if the AI Hive service is trusted, use non-sensitive reference images, protect the API key, and review the skill before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-detail-page-image-set-generation)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses approved product references, prompts, model parameters, task IDs, and a local output directory for generated images.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
