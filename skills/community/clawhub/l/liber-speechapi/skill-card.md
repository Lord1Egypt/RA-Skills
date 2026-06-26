## Description: <br>
Liber SpeechAPI handles Telegram voice-message workflows with ASR, concise reply summarization, and Telegram-compatible TTS, and also supports direct text-to-speech and speech-to-text tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent to a configured Liber SpeechAPI backend for ASR, TTS, and Telegram voice reply workflows. It is useful when an agent needs to transcribe audio, synthesize spoken replies, or return structured speech-processing results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio, transcripts, TTS text, and voice-clone reference audio are sent to a configured Liber SpeechAPI backend. <br>
Mitigation: Use only a trusted HTTPS backend and review its data handling before sending sensitive voice or transcript content. <br>
Risk: The skill requires LIBER_API_BASE_URL and LIBER_API_KEY credentials. <br>
Mitigation: Provide credentials from a trusted secret source, avoid workspace .env files for sensitive keys, and do not print or log API keys. <br>
Risk: Voice cloning can use reference audio from a configured file. <br>
Mitigation: Enable voice cloning only with clear permission from the speaker and omit clone audio when permission or provenance is unclear. <br>
Risk: The workflow depends on an external backend service and optional setup scripts. <br>
Mitigation: Review the backend and its setup scripts before deployment, then verify health checks and authentication against the intended service. <br>


## Reference(s): <br>
- [Liber SpeechAPI Reference](references/api.md) <br>
- [Configuration](references/config.md) <br>
- [Liber SpeechAPI Parameters](references/parameters.md) <br>
- [Telegram / openclaw Workflow](references/workflow.md) <br>
- [Liber SpeechAPI upstream project](https://github.com/liberalchang/Liber_SpeechAPI) <br>
- [insanely-fast-whisper](https://github.com/Vaibhavs10/insanely-fast-whisper) <br>
- [chatterbox](https://github.com/resemble-ai/chatterbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Text, JSON, Markdown guidance, and audio result URLs or local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [ASR defaults to structured JSON; TTS returns an audio URL and may save a local audio file; Telegram replies use OGG/Opus.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
