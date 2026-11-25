## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6，要为商品做场景图、生活方式图、换背景、场景合成或营销展示时使用。按平台规范拆分任务并写好提示词，报价经用户确认后出图；没有 CLI 或密钥时交付可直接提交的出图方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营者、商品营销团队和设计人员可用此技能，将商品参考图制作成生活方式场景图、背景替换图或营销图。未配置 CLI 或密钥时，技能会提供可直接提交的提示词和参数方案。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged suspicious because its setup instructions use an unpinned CLI with installation confirmation skipped; scanner coverage was partial and the analysis incomplete.

Mitigation: Review and pin the CLI version before installation, check the commands, permissions, and credentials it will use, and resolve the reported local path-like references. The partial scan does not establish that the skill is safe.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2-6-scene-image)
- [Publisher profile](https://clawhub.ai/user/autoagc)

## Skill Output:

**Output Type(s):** [Images, Guidance, Markdown, JSON]

**Output Format:** [Generated image files, or a Markdown image plan with prompts and JSON parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When images cannot be generated, provide a complete, directly submitable plan; do not claim images were generated or invent task IDs, links, or charges.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
