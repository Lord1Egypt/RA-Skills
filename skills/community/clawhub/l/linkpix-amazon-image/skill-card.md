## Description:

帮助亚马逊卖家和电商团队通过青虎 AI 生成商品主图、套图、A+ 页面图和活动图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

亚马逊卖家、跨境电商美工和外贸团队可用它制作纯白底主图、商品套图、A+ 页面图、卖点图及促销图片，并按目标站点调整语言和视觉内容。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance asks users to share an API key in chat.

Mitigation: Configure the key locally in qhkit or an environment variable; do not post it in chat, and replace any key already shared.

Risk: The setup guidance installs and upgrades command-line software.

Mitigation: Review the package version and installation path, and install in an isolated environment without administrator access.

Risk: Selected images are uploaded to Qinghu AI, and generation consumes credits.

Mitigation: Confirm the selected images and expected cost before submitting a generation request.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix ClawHub release](https://clawhub.ai/autoagc/skills/linkpix-amazon-image)

## Skill Output:

**Output Type(s):** [Images, Text]

**Output Format:** [Generated product images with task results and download links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image count, model, size, quality, and language depend on the selected workflow and available options.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
