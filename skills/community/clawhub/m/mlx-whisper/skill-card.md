## Description: <br>
Local speech-to-text with MLX Whisper (Apple Silicon optimized, no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kevin37Li](https://clawhub.ai/user/Kevin37Li) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to run local speech-to-text, translation, and subtitle generation workflows with MLX Whisper on Apple Silicon Macs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on the mlx-whisper pip package and selected Hugging Face model sources. <br>
Mitigation: Install only from trusted package and model sources, and pin or review the selected package and model before use in managed environments. <br>
Risk: Model downloads can be large and are cached locally. <br>
Mitigation: Confirm sufficient disk space and manage the Hugging Face cache according to local retention and storage policies. <br>
Risk: Audio or video inputs may contain sensitive speech or personal information. <br>
Mitigation: Only process media files that are approved for local transcription or translation on the target machine. <br>


## Reference(s): <br>
- [MLX Whisper examples](https://github.com/ml-explore/mlx-examples/tree/main/whisper) <br>
- [ClawHub release page](https://clawhub.ai/Kevin37Li/mlx-whisper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on local CLI transcription, translation, subtitle generation, model selection, and installation requirements.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
