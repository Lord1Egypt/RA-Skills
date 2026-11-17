## Description:

使用 AI Hive 的 Seedance 2.5 生成、编辑和延长视频，并把可灵 Kling 工作流迁移为镜头控制表以保留镜头运动、主体锁定、动作节拍和交付比例。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and video production teams use this skill to translate Kling-style text-to-video, image-to-video, reference-video, editing, and extension workflows into AI Hive Seedance 2.5 commands with shot-control guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script performs network uploads/downloads and trusts server-supplied URLs and filenames too broadly.

Mitigation: Review before installing, use only media intended for AI Hive, run in a limited workspace or virtual environment, prefer --no-download or a dedicated output directory for untrusted tasks, and avoid sensitive networks until URL validation and output-path containment are added.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/kling-video-generation-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)
- [Publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown with inline bash code blocks and JSON task responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI Hive video generation tasks and return task IDs; downloads can be disabled with --no-download.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
