## Description:

Local speech-to-text with Parakeet MLX (ASR) for Apple Silicon (no API key).

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylehowells](https://clawhub.ai/user/kylehowells)

### License/Terms of Use:


## Use Case:

Developers, engineers, and transcription users use this skill to have an agent run local speech-to-text transcription on Apple Silicon with the Parakeet MLX CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unpinned third-party CLI package from the configured Python package source.

Mitigation: Install only from trusted package sources and pin a reviewed parakeet-mlx version for controlled environments.

Risk: The transcription CLI reads local audio files and downloads model files into the local Hugging Face cache.

Mitigation: Review audio-file sensitivity before use and manage the local model cache according to the deployment environment's data-handling policy.

## Reference(s):

- [Parakeet MLX GitHub repository](https://github.com/senstella/parakeet-mlx)
- [ClawHub skill page](https://clawhub.ai/kylehowells/skills/parakeet-mlx)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local CLI transcription that can produce txt, srt, vtt, json, or all supported output formats.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
