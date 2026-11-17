## Description:

Local speech-to-text with MLX Whisper (Apple Silicon optimized, no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin37li](https://clawhub.ai/user/kevin37li)

### License/Terms of Use:


## Use Case:

Developers and users on Apple Silicon Macs use this skill to transcribe local audio, translate speech to English, and generate SRT subtitle files with the mlx_whisper command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned Python command-line dependency with pip.

Mitigation: Install in an isolated environment and prefer a pinned, reviewed mlx-whisper package version when available.

Risk: Whisper models are downloaded on first use and cached locally.

Mitigation: Use approved model sources and account for local cache storage under ~/.cache/huggingface/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevin37li/skills/mlx-whisper)
- [MLX Whisper project reference](https://github.com/ml-explore/mlx-examples/tree/main/whisper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the mlx_whisper command-line binary; expected downstream outputs include transcription text, translation text, or SRT subtitle files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
