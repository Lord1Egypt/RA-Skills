## Description:

在底轨素材铺齐并完成构图确认后，按派单驱动栏目生产 skill 生成动态图颗粒，并通过 gtrk CLI 检查后铺入工程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitruck](https://clawhub.ai/user/gitruck)

### License/Terms of Use:

MIT-0

## Use Case:

面向使用 Gitruck 剪辑工作流的创作者与剪辑人员，在底轨和构图确认后，将按派单生成的动态图颗粒检查并铺入视频工程。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud rendering can incur costs and involve sharing project data.

Mitigation: Review expected rendering costs and data sharing before using cloud steps.

Risk: Rebuilding generated overlays can overwrite manual project adjustments.

Mitigation: Keep a project backup before rebuilding overlays.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/gitruck/skills/gtrk-mg)
- [Gitruck CLI project (metadata homepage)](https://github.com/Gitruck/cli)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [CLI actions and project timeline updates, with concise text status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update a .gtrk project by laying validated MG overlays onto its beat track.]

## Skill Version(s):

1.3.10 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
