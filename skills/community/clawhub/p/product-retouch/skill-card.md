## Description:

使用 GPT Image 2 精修现有商品照片，以缺陷清单和不可变项控制除尘、去划痕、反光整理、颜色校准、标签保护与背景清理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, product photographers, and marketplace teams use this skill to retouch existing product photos while preserving product shape, labels, logos, color baselines, packaging counts, and truthful wear or damage signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected product photos and prompts are sent to AI Hive for processing.

Mitigation: Use the skill only with data approved for AI Hive, avoid sensitive unreleased product imagery unless the service is approved for that data, and use a dedicated API key.

Risk: Upload and download handling relies on remote server-provided URLs.

Mitigation: Run the skill in an isolated environment and review or constrain returned upload and download domains before operational use.

Risk: Retouching could hide product condition details that affect purchasing decisions.

Mitigation: Keep a defect register, require merchant approval for material condition changes, and preserve truthful wear, missing parts, labels, logos, and product structure.

## Reference(s):

- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-retouch)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Images]

**Output Format:** [Markdown guidance with bash commands; task queries return JSON and completed image jobs download PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one reference image, an AI Hive API key, and the fixed public_model_gpt_image_2 image model.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
