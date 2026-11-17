## Description:

为粗剪视频的选定时间窗设计并生成合成画面，支持整片铺满、AI 推荐或指定区间。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitruck](https://clawhub.ai/user/gitruck)

### License/Terms of Use:

MIT-0

## Use Case:

视频剪辑人员可在粗剪、B-roll 和字幕确定后，为选定时间窗设计画面合成，并通过 gtrk 工作流构建、检查和铺设合成片段。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The rapid-production handoff applies project edits before final review, which can leave an unsuitable composite in the project.

Mitigation: Keep a project backup and use stepwise mode to review each change before it is applied.

Risk: A failed local bake leaves that segment using the rough-cut footage in the rendered video.

Mitigation: Check the bake results and resolve failed windows before delivering the finished video.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/gitruck/skills/gtrk-composite)
- [Gitruck CLI](https://github.com/Gitruck/cli)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance, HTML scene files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Window-by-window design and review guidance; scene files are built and checked before project changes are applied.]

## Skill Version(s):

1.3.9 (source: server-resolved release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
