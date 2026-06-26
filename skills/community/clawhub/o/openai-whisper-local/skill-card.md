## Description: <br>
Local speech-to-text with the Whisper CLI (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wingchiu](https://clawhub.ai/user/wingchiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run local Whisper CLI transcription or translation for user-provided audio without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on Homebrew to install the openai-whisper CLI. <br>
Mitigation: Install only in environments where Homebrew and the openai-whisper formula are trusted and appropriate. <br>
Risk: Whisper models are downloaded and cached locally on first use. <br>
Mitigation: Confirm local storage policy and available disk space before first transcription, especially on shared or managed machines. <br>
Risk: Audio recordings and transcript outputs may contain sensitive information. <br>
Mitigation: Choose input files and output directories deliberately and handle generated transcript files according to the user's data policy. <br>


## Reference(s): <br>
- [OpenAI Whisper](https://openai.com/research/whisper) <br>
- [OpenAI Whisper Local on ClawHub](https://clawhub.ai/wingchiu/openai-whisper-local) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcription output is produced locally by the Whisper CLI, commonly as txt or srt files, with models cached under ~/.cache/whisper on first use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
