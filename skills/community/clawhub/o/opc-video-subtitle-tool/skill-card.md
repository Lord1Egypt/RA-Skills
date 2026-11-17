## Description:

Adds voiceover and styled subtitles to videos through a Coze workflow, with preset or custom subtitle styles, voice selection, and speech speed controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to add Chinese voiceover and subtitles to videos, select one of eight subtitle presets, or customize subtitle colors and speech speed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package ships an exposed Coze API credential.

Mitigation: Remove or rotate the embedded credential and require runtime credentials from a secure environment variable before installation or execution.

Risk: Video URLs and subtitle text are sent to a third-party Coze workflow.

Mitigation: Document the data flow clearly and obtain user consent before sending video or text data to external processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/opc-video-subtitle-tool)
- [Subtitle styles configuration](references/subtitle-styles.md)
- [Coze platform](https://coze.cn)
- [Voice options reference](https://x2hx0ilo74.feishu.cn/wiki/QJCVwnbr1iBOkzkllk6cS6tCnZe)
- [Subtitle field details](https://my.feishu.cn/wiki/TumOwWKFNiTr19ky36Vc7bXZnLc)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a processed video URL when the Coze workflow succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
