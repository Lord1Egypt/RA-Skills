## Description:

通过 LinkPix 将视频中的人物替换为参考图片中的角色，同时保留原视频的动作和口型。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要视频换人、换模特或跨市场广告本地化的创作者和营销人员，使用原视频与参考人物图片生成角色替换视频。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video and reference images are uploaded to the qhkit/LinkPix service.

Mitigation: Confirm the user is comfortable sending these materials to the service before submission.

Risk: Replacing a real person's likeness without permission can enable deceptive or unauthorized use.

Mitigation: Confirm authorization for any real person's likeness; decline unauthorized face replacement.

Risk: The skill can install or update Node and qhkit in persistent user locations and change token configuration.

Mitigation: Prefer a preinstalled, pinned qhkit binary; obtain explicit approval before global installs, upgrades, PATH changes or token storage.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-video-role-swap)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command examples and a generated video link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports task status, the video URL and charged credits when available.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
