## Description:

帮助电商商家通过青虎AI制作阿里Wanx 3.0商品展示和带货短视频，涵盖素材上传、任务查询与成片交付。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

淘宝、天猫和1688商家及运营团队用它制作商品主图、活动推广和信息流广告短视频。技能帮助选择可用模型、估算积分并在用户确认后提交生成任务。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool requires an API key that may be stored in local configuration.

Mitigation: Share the key only if comfortable with the tool's access; protect it and avoid exposing it in shared logs.

Risk: Selected product images or videos are uploaded to the service.

Mitigation: Review media for confidential or sensitive content before uploading.

Risk: Video generation can consume paid credits.

Mitigation: Review estimated credits and generation parameters, then require explicit approval before submission.

Risk: Installing command-line dependencies or persisting PATH changes affects the local environment.

Mitigation: Prefer pinned dependency versions and keep PATH changes session-scoped unless persistence is intended.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-wanx-3-sales)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [青虎AI API key guide](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task status, generated video links and credit usage when available.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
