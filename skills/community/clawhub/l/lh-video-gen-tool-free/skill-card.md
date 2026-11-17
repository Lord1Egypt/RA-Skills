## Description:

从Markdown脚本一键生成9:16竖版短视频，支持TTS配音、字幕烧录与画面同步，适合个人内容创作者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and developers use this skill to turn Markdown scripts into single 9:16 short videos with TTS narration, subtitle cards, synchronized timing, and MP4 composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom TTS command templates can enable broad command execution despite the artifact's whitelist claim.

Mitigation: Install only in trusted workflows, review every --tts-command value before execution, and prefer fixed, well-known TTS commands with carefully quoted arguments.

Risk: Untrusted scripts or speech text used with custom command templates may increase command execution risk.

Mitigation: Avoid untrusted Markdown scripts and speech text when custom TTS templates are enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/lh-video-gen-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create MP4 videos, subtitle images, TTS audio clips, and temporary media assets through FFmpeg, browser screenshot, and TTS tooling.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
