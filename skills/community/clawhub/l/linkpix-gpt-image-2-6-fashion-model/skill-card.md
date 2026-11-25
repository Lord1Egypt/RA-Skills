## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6，要做电商模特图、试穿、模特换装或用获授权的人像参考替换模特脸部时使用。按平台规范拆分任务并写好提示词，报价经用户确认后出图；没有 CLI 或密钥时交付可直接提交的出图方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

服饰电商从业者和内容创作者可用此技能规划模特试穿、换装及穿搭图，并在具备工具与凭据时生成图片；否则获得可直接提交的提示词和参数方案。

### Deployment Geography for Use:

China (the documented qhkit workflow requires the cn site)

## Known Risks and Mitigations:

Risk: The documented install uses a mutable package release that may change.

Mitigation: Review the package and version before installation, and pin a reviewed release where practical.

Risk: Scanner coverage was partial because three referenced local paths could not be resolved.

Mitigation: Resolve and review the referenced local files before relying on behavior that the scan could not cover.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Images]

**Output Format:** [Markdown prompts and JSON parameters; generated image files when image generation succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation depends on an available CLI, credentials, user approval of the estimate, and successful service execution.]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
