## Description:

帮助电商团队和商业内容创作者使用 HappyHorse 1.1 生成商品展示、广告与带货视频，并可用图片、视频或音频控制生成结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营、品牌和商业内容团队可用此技能按商品卖点制作带货短视频、广告和产品展示视频，并可提供图片、视频或音频作为控制素材。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions use unpinned package downloads that can be fetched and run.

Mitigation: Review the package and pin an exact @iqinghu/qhkit version before installing or invoking it.

Risk: Setup instructions ask users to share an API key in chat, creating credential exposure risk.

Mitigation: Configure the API key locally through a secure credential method or environment variable, and do not paste it into chat.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-happyhorse-sales)

## Skill Output:

**Output Type(s):** [Video, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated video files or URLs, with text or JSON task status and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video duration, orientation, and reference media depend on the selected model and its available options.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
