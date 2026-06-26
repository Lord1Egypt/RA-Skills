## Description: <br>
Local speech-to-text using whisper-cli (whisper.cpp). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuxxin](https://clawhub.ai/user/wuxxin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to transcribe local audio files with whisper-cli and the large-v3-turbo whisper.cpp model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup command downloads a model from Hugging Face into /usr/share, which may require elevated local permissions. <br>
Mitigation: Verify the model source and checksum before installation, and use normal local change-control practices before writing to system directories. <br>
Risk: The wrapper depends on the locally installed whisper-cli binary and model path. <br>
Mitigation: Confirm whisper-cli is installed and that the expected model file exists before running transcription commands. <br>


## Reference(s): <br>
- [ggml-large-v3-turbo model download](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin?download=true) <br>
- [Local Whisper (cpp) on ClawHub](https://clawhub.ai/wuxxin/local-whisper-cpp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and transcription text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires whisper-cli and a local model file at /usr/share/whisper.cpp-model-large-v3-turbo/ggml-large-v3-turbo.bin.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
