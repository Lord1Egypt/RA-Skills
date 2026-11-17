## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6，要做电商模特图、试穿、模特换装或用获授权的人像参考替换模特脸部时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商服饰团队可用此技能依据服装图和获授权的模特参考图制作虚拟试穿、换装或换脸图片，并检查商品细节与输出规格。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images may depict people whose likeness you are not authorized to use.

Mitigation: Upload only images you are authorized to use with Qinghu.

Risk: An incorrectly configured account or service address can expose credentials or route work to the wrong service.

Mitigation: Verify the configured Qinghu account and service address, and keep API keys out of task files and replies.

Risk: Image generation uses account credits.

Mitigation: Review the estimated credits before confirming generation.

Risk: The external qhkit CLI is outside the bundled-code review, and installing @latest may change its implementation.

Mitigation: Check the installed CLI version and review the package before upgrading it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2-6-fashion-model)
- [青虎 API Keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Images, JSON, Guidance, Shell commands, Configuration]

**Output Format:** [Generated image files and JSON results; Markdown guidance and editable prompts when generation is unavailable]

**Output Parameters:** [Variable by selected image count and size preset]

**Other Properties Related to Output:** [Prompt limit: 5,000 characters. Verify actual image dimensions, format, and count against the selected options.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
