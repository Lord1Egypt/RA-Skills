## Description:

使用 gtrk CLI 将歌曲与可选背景或封面制作成频谱可视化视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitruck](https://clawhub.ai/user/gitruck)

### License/Terms of Use:

MIT-0

## Use Case:

音乐人、创作者和内容制作人员可用它把本地歌曲制作成带频谱动画的视频，并按需添加背景、封面、曲目信息和配色。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio and optional background or cover media are uploaded to Gitruck Cloud, and video generation is charged by duration.

Mitigation: Upload only media you are comfortable sharing with the service, and confirm the expected duration-based cost before generation.

Risk: Cloud steps may use a Gitruck API key, and project edits can affect existing work.

Mitigation: Protect the API key, review the installed CLI version, and back up the project before making edits.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/gitruck/skills/gtrk-music-visualizer)
- [Gitruck CLI homepage](https://github.com/Gitruck/cli)

## Skill Output:

**Output Type(s):** [Video files, JSON, Shell commands, Guidance]

**Output Format:** [MP4 video and JSON result manifest, with CLI commands and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output location and video settings can be selected; generation uses a cloud service and is duration-priced.]

## Skill Version(s):

1.3.9 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
