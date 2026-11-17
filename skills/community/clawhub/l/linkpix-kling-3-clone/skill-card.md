## Description:

帮助短视频创作者拆解参考视频的镜头与节奏，改写成商品脚本，并通过青虎 AI 生成可灵 3.0 风格的视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

短视频创作者、电商卖家及运营人员可用此技能分析参考视频、改写商品脚本，并在确认参数与费用后生成营销视频。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference media and links are uploaded to the qhkit service.

Mitigation: Use only media you are authorized to share, and avoid highly sensitive content.

Risk: API token setup can persist access to the qhkit service.

Mitigation: Keep the token private and revoke or rotate it when no longer needed.

Risk: Unpinned qhkit installs may change the code being run.

Mitigation: Review or pin the qhkit package version before installation when possible.

Risk: Generating a video consumes credits and submitted tasks cannot be canceled.

Mitigation: Review the model, media, duration, and estimated credits; require explicit approval before submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-kling-3-clone)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [青虎 AI API 密钥指南](https://xcnzsfe4uxrw.feishu.cn/wiki/KJ0Ywsyw8iAXmRkz5l4cddDbn6g)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with script comparisons, shell commands, and generated video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation requires user confirmation; completed tasks return a video link and credit usage.]

## Skill Version(s):

0.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
