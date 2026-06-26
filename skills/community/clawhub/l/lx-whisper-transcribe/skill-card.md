## Description: <br>
Transcribes audio to text for OpenClaw using a local Whisper-based workflow with Chinese language support and no API key requirement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxuebin20260309](https://clawhub.ai/user/liuxuebin20260309) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to transcribe voice messages or audio files into text, especially Chinese speech, with local model execution and no API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup may download transcription models from hf-mirror.com or Hugging Face. <br>
Mitigation: Review and verify model sources before use, and use an approved mirror or cache for managed environments. <br>
Risk: Installation guidance creates a persistent ~/bin/whisper wrapper and may append ~/bin to ~/.bashrc. <br>
Mitigation: Prefer a temporary PATH or virtual environment during evaluation, and remove the wrapper and shell profile entry when no longer needed. <br>
Risk: The artifact describes whisper.cpp, while the setup guide uses a Python faster_whisper wrapper. <br>
Mitigation: Review the actual installed wrapper and Python dependencies before relying on the transcription path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuxuebin20260309/lx-whisper-transcribe) <br>
- [OpenClaw speech-to-text usage guide](SHARE_GUIDE.md) <br>
- [Hugging Face](https://huggingface.co) <br>
- [hf-mirror.com](https://hf-mirror.com) <br>
- [whisper.cpp tiny model download](https://hf-mirror.com/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text transcription with Markdown setup guidance and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to Chinese transcription with a tiny model and CPU execution; first use may download model files.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
