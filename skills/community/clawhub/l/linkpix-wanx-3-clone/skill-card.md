## Description:

帮助电商短视频团队分析热门视频的节奏、卖点和脚本结构，并改写为适配淘宝内容渠道的短视频脚本与成片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商短视频团队可用它从参考视频提炼镜头节奏和卖点，再改写为适配淘宝逛逛、点淘等渠道的商品脚本并生成短视频。

### Deployment Geography for Use:

中国大陆

## Known Risks and Mitigations:

Risk: Unpinned packages may run during setup.

Mitigation: Review the packages and pin versions before installation, following the security guidance.

Risk: The setup guidance asks users to share an API key in chat.

Mitigation: Configure the key locally through a secure environment variable or local CLI configuration; do not send it in chat.

Risk: Scanner coverage is partial because a referenced local path could not be resolved.

Mitigation: Resolve and review the missing path, then repeat the security review before relying on the scan.

## Reference(s):

- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Analysis, Text, Video]

**Output Format:** [Markdown scripts and generated video files or links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video duration is selected from available model options (5–30 seconds where supported).]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
