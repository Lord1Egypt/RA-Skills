## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6 制作 Amazon 亚马逊 Listing 主图、副图或 A+ 页面素材时使用。按平台规范拆分任务并写好提示词，报价经用户确认后出图；没有 CLI 或密钥时交付可直接提交的出图方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

亚马逊跨境卖家可用此技能规划商品主图、副图和 A+ 页面素材，生成逐图提示词及可提交的参数配置；环境就绪时，先核对报价并经用户确认后再生成图片。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs and runs qhkit from a mutable latest release, creating a software supply chain risk.

Mitigation: Pin qhkit to a reviewed release and control its installation before running the workflow.

Risk: The scan had partial reference resolution because several local path-like references were missing, so it does not establish safety for those references.

Mitigation: Resolve and review the missing references before relying on the scan result or running the workflow.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-gpt-image-2-6-amazon-image)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance, Image files]

**Output Format:** [中文 Markdown 出图方案与提示词、JSON 参数文件；环境就绪并经报价确认后可交付生成的图片文件]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [按商品、版位和画幅拆分任务；报价确认前不生成图片，并在无法出图时提供完整可提交方案。]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
