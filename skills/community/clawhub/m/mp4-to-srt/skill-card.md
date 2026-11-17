## Description:

Converts local MP4, MKV, or AVI videos into SRT subtitle files and automatically converts subtitles to Traditional Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dolphins1123](https://clawhub.ai/user/dolphins1123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media producers use this skill to guide local conversion of video files into standard SRT subtitles using Whisper, with optional model selection and Traditional Chinese conversion through OpenCC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation may introduce environment or supply-chain risk.

Mitigation: Use a virtual environment and pinned dependency versions when installing Whisper and related tooling.

Risk: Generated subtitle files may be written into shared or untrusted directories.

Mitigation: Choose an output path in a trusted local directory and review generated files before sharing or importing them.

Risk: Subtitles are converted to Traditional Chinese by default.

Mitigation: Install only when that default behavior is desired, or explicitly disable conversion where the script interface supports it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dolphins1123/skills/mp4-to-srt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for generating local SRT subtitle files; runtime output depends on installed ffmpeg, Whisper, and OpenCC dependencies.]

## Skill Version(s):

1.1.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
