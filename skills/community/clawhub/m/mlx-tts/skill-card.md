## Description:

Text-To-Speech with MLX (Apple Silicon) and opensource models (default QWen3-TTS) locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqiao](https://clawhub.ai/user/guoqiao)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate local text-to-speech audio on Apple Silicon Macs with MLX and open-source models, then return the generated OGG audio file as voice-message output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can modify the host environment and install an unpinned prerelease-capable mlx-audio package.

Mitigation: Review the installer before use and prefer pinned or manual dependency installation in controlled environments.

Risk: Broad trigger phrases can invoke the skill and create or send an audio file.

Mitigation: Confirm user intent before generating or sending voice-message output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqiao/skills/mlx-tts)
- [ClawHub metadata homepage](https://clawhub.ai/guoqiao/mlx-tts)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Plain-text file path to a generated OGG audio file, with guidance for sending it as a voice message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a temporary output directory and requires macOS on Apple Silicon with Homebrew, ffmpeg, uv, and mlx-audio available or installed.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
