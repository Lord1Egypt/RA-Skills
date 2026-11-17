## Description:

Guides agents in using the MetaDig CLI to generate and manage AI images, video, speech, and music.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pythonthink](https://clawhub.ai/user/pythonthink)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the skill to choose MetaDig models and parameters, submit media-generation tasks, check progress, download results, and organize outputs into projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and repair instructions run changing internet scripts, and the external installer and CLI were not verified.

Mitigation: Review the installer, use a fixed CLI release with independently verified integrity, and avoid automatically rerunning downloaded installers during troubleshooting.

Risk: Reference media is uploaded and receives public URLs.

Mitigation: Use only media you are permitted to share publicly.

Risk: Media generation spends account credits.

Mitigation: Check current model pricing and estimate the credit cost before submitting generation tasks.

## Reference(s):

- [MetaDig CLI documentation](https://waytometa.cn/docs/skills/agent-skill)
- [MetaDig CLI](https://waytometa.cn/cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Images, Video, Speech audio, Music audio]

**Output Format:** [Markdown instructions and CLI task results or generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media uses account credits; selected reference media is uploaded and receives public URLs.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
