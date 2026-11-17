## Description:

Speech-To-Text with MLX (Apple Silicon) and opensource models (default GLM-ASR-Nano-2512) locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqiao](https://clawhub.ai/user/guoqiao)

### License/Terms of Use:


## Use Case:

Developers and external users on Apple Silicon Macs use this skill to transcribe local audio files to text with MLX and open-source models, without an API key or remote server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer force-installs mlx-audio with prerelease versions allowed, which can change installed behavior over time.

Mitigation: Review the installer before use and prefer a pinned stable mlx-audio version for controlled deployments.

Risk: Confidential audio may be converted into temporary files and transcript files during execution.

Mitigation: Run the skill only in trusted local environments and clean temporary files after interrupted or failed runs.

Risk: Broad natural-language triggers could activate transcription workflows when the user only intended discussion or review.

Mitigation: Require explicit confirmation of the audio file path and intended transcription action before running shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqiao/skills/mlx-stt)
- [Source homepage](https://github.com/guoqiao/skills/blob/main/mlx-stt/mlx-stt/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text transcript and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcript is printed to stdout after local audio conversion and model execution.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
