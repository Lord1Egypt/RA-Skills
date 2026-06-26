## Description: <br>
Configures local Whisper speech recognition with whisper.cpp so agents can convert Feishu, Telegram, and other voice messages into text offline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[279458179](https://clawhub.ai/user/279458179) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up offline speech-to-text on Linux servers, including dependency installation, whisper.cpp build steps, model selection, audio conversion, transcription commands, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing packages and building whisper.cpp can affect the host system. <br>
Mitigation: Install only on machines where package installation and local builds are acceptable, and pin whisper.cpp to a trusted release or commit where possible. <br>
Risk: Voice files and transcripts may contain private information. <br>
Mitigation: Use unique restricted temporary filenames instead of shared paths such as /tmp/audio.wav, and delete audio and transcript files after processing when they may contain sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/279458179/openclaw-whisper-asr) <br>
- [whisper.cpp official documentation](https://github.com/ggml-org/whisper.cpp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local setup steps, model choices, audio conversion commands, transcription commands, paths, troubleshooting, and quantization guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
