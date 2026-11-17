## Description:

编排 gtrk CLI，将带现场同期声的视频素材整理为可审阅脚本与纪实 Vlog 成片工程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitruck](https://clawhub.ai/user/gitruck)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者可用此技能梳理带现场声音的视频素材、组织故事线并编排剪辑步骤，制作纪实风格的 Vlog 工程。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud narration and highlight analysis may send approved text or source audio to an external provider, depending on the selected operation.

Mitigation: Use a dedicated media folder, review the provider's privacy terms, and use --no-audio for highlight analysis when source audio is private.

Risk: Narration generation can incur charges.

Mitigation: Review the script and estimated charges, and approve paid narration generation before it runs.

## Reference(s):

- [Gitruck CLI](https://github.com/Gitruck/cli)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, JSON configuration, Video editing project]

**Output Format:** [Markdown guidance with shell commands and JSON project manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a structured audiovisual script and editing project for review and rendering in the client.]

## Skill Version(s):

1.3.10 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
