## Description: <br>
Speech-To-Text with MLX (Apple Silicon) and opensource models (default GLM-ASR-Nano-2512) locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqiao](https://clawhub.ai/user/guoqiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users on macOS with Apple Silicon use this skill to transcribe local audio files with MLX and open-source speech-to-text models without an API key or remote server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation pulls or updates external command-line dependencies with Homebrew and uv, including mlx-audio. <br>
Mitigation: Install only in environments where those local tool changes are acceptable and review dependency changes before use. <br>
Risk: Transcripts are printed into the agent session and may contain sensitive audio content. <br>
Mitigation: Use explicit audio paths and avoid transcribing files containing information that should not enter the agent context. <br>


## Reference(s): <br>
- [MLX STT source homepage](https://github.com/guoqiao/skills/blob/main/mlx-stt/mlx-stt/SKILL.md) <br>
- [MLX STT ClawHub listing](https://clawhub.ai/guoqiao/mlx-stt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text transcript printed to stdout with shell command usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS on Apple Silicon, Homebrew, ffmpeg, uv, and mlx-audio; first run may download the model.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
