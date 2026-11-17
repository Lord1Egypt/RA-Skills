## Description:

使用 AI Hive Seedance 2.5 迁移海螺 AI、Hailuo AI 或 MiniMax 海螺常见的叙事视频需求，覆盖文生、图生、角色参考、表演编辑和镜头延长，重点控制人物动机、动作因果与情绪连续；不是海螺官方服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to guide AI agents through AI Hive Seedance 2.5 video generation, image-to-video, reference-to-video, video editing, and video extension workflows for narrative clips. It emphasizes character motivation, visible action, reactions, continuity checks, and authorized source materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a suspicious verdict because API-supplied download naming can write files outside the chosen output folder.

Mitigation: Review before installing, run in an isolated Python environment, and avoid output directories where unintended file creation or overwrite would matter until filename sanitization is fixed.

Risk: The skill requires trust in the AI Hive endpoint and stores or reads an AI Hive API key locally.

Mitigation: Use only trusted AI Hive credentials, prefer the AI_HIVE_API_KEY environment variable or a permission-restricted config file, and rotate keys if exposure is suspected.

Risk: Video editing and reference workflows can misuse unlicensed source media or produce continuity errors.

Mitigation: Use authorized images and videos, archive source-material permissions and task IDs, and review generated video seams, identity continuity, clothing, props, gaze, and action timing before publication.

## Reference(s):

- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/hailuo-video-generation-alternative)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI Hive video tasks, poll task status, upload media, and download generated media files when executed with a valid AI Hive API key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
