## Description:

帮助京东运营团队通过青虎 AI 制作商品主图套图、详情页长图和营销活动海报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

京东运营人员、广告优化师和品牌团队可用此技能，将商品参考图制作成适配京东、京东国际或京喜的主图套图、详情页图片和活动海报。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The supplied security summary flags unpinned package installation that may run with the agent’s permissions.

Mitigation: Review the package installation steps, assess trust in the unpinned package, and limit the skill to the access it needs.

Risk: The supplied security summary notes setup instructions that request an API key in chat.

Mitigation: Do not share the API key in chat; configure it through an appropriately protected secret or environment variable.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [LinkPix JD image skill listing](https://clawhub.ai/autoagc/skills/linkpix-jd-image)

## Skill Output:

**Output Type(s):** [Image files, Configuration guidance, Shell commands]

**Output Format:** [Generated product image files with Markdown setup and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image count, model, size, and styling depend on the selected options and user-provided product image or copy.]

## Skill Version(s):

0.1.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
