## Description:

口播竖屏视频加工流程：可选人像精修，并按口播时序叠加图片素材，同时保留原声。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jes614753-sketch](https://clawhub.ai/user/jes614753-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

面向视频创作者和剪辑人员，用于精修口播人物画面，并按讲述内容将证据图、截图或标识叠加到竖屏视频中。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow deletion steps could affect files the user wants to keep.

Mitigation: Review the target paths and deletion commands before running the workflow, and keep a backup of important files.

Risk: The optional cloud processing route has a reported privacy gap for video containing a person's face or voice.

Mitigation: Use local processing where practical; before uploading footage, confirm that the service and data handling are acceptable for that material.

Risk: Security scan coverage is partial, so available results do not establish that all behavior was assessed.

Mitigation: Review the workflow before installation and execution, especially file deletion and any cloud processing steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jes614753-sketch/skills/koubo-video-overlay)
- [人像精修指南](references/face-refine.md)
- [视频加工踩坑与解法](references/pitfalls.md)
- [FaceFusion](https://github.com/facefusion/facefusion)
- [CodeFormer](https://github.com/sczhou/CodeFormer)
- [GFPGAN](https://github.com/TencentARC/GFPGAN)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with code snippets and video-processing configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Steps depend on the source video's dimensions, frame rate, overlay assets, and timing.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
