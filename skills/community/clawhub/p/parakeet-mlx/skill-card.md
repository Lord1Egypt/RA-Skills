## Description: <br>
Local speech-to-text with Parakeet MLX (ASR) for Apple Silicon (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylehowells](https://clawhub.ai/user/kylehowells) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other users can use this skill to transcribe local audio files on Apple Silicon with the Parakeet MLX command-line tool. It supports common transcript outputs such as txt, srt, vtt, json, or all formats at once. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and running third-party transcription dependencies can introduce package or binary supply-chain risk. <br>
Mitigation: Install only from trusted sources and verify the parakeet-mlx package, ffmpeg installation, and Hugging Face model source before use. <br>
Risk: Models are downloaded and cached locally on first use. <br>
Mitigation: Plan for local Hugging Face cache creation and only process audio files intended for transcription. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kylehowells/parakeet-mlx) <br>
- [Parakeet MLX project homepage](https://github.com/senstella/parakeet-mlx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers local transcription commands and output formats including txt, srt, vtt, json, and all.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
