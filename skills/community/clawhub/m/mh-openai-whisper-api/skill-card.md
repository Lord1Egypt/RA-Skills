## Description: <br>
Transcribe audio via OpenAI Audio Transcriptions API (Whisper). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to transcribe a selected local audio file through OpenAI's audio transcription API and save the result as text or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are uploaded to OpenAI for transcription. <br>
Mitigation: Use only audio that policy permits sending to OpenAI; avoid confidential, regulated, or third-party recordings unless that upload is allowed. <br>
Risk: The skill requires an OPENAI_API_KEY for API access. <br>
Mitigation: Provide the API key through the expected environment or configuration path and avoid exposing it in shared logs, commands, or artifacts. <br>


## Reference(s): <br>
- [OpenAI Speech to Text Guide](https://platform.openai.com/docs/guides/speech-to-text) <br>
- [OpenAI Audio Transcriptions API Endpoint](https://api.openai.com/v1/audio/transcriptions) <br>
- [ClawHub Skill Page](https://clawhub.ai/mohdalhashemi98-hue/mh-openai-whisper-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Plain text transcript or JSON transcription file, with the output path printed by the shell command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, OPENAI_API_KEY, and a user-selected audio file; optional flags control model, language, prompt, response format, and output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
