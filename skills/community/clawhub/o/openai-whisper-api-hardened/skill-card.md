## Description: <br>
Transcribe audio via OpenAI Audio Transcriptions API (Whisper). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe selected local audio files through OpenAI's Audio Transcriptions API using a curl-based wrapper. It supports plain text or JSON transcript output with optional model, language, prompt, and output-path settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports an input-handling flaw that could unintentionally send local file contents to OpenAI. <br>
Mitigation: Avoid untrusted or file-derived --prompt, --model, and --language values, especially values that start with @ or <, until the wrapper uses literal form fields. <br>
Risk: The skill requires OPENAI_API_KEY and can expose credentials if agents display environment variables or credential files. <br>
Mitigation: Check only whether credentials are present and never print, encode, transfer, or display API keys or credential-containing files. <br>
Risk: Selected audio files are transmitted to OpenAI for transcription. <br>
Mitigation: Use the skill only for audio the operator is comfortable sending to OpenAI, with appropriate permission and data handling review. <br>


## Reference(s): <br>
- [OpenAI Speech to Text Documentation](https://platform.openai.com/docs/guides/speech-to-text) <br>
- [OpenAI Audio Transcriptions API Endpoint](https://api.openai.com/v1/audio/transcriptions) <br>
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/openai-whisper-api-hardened) <br>
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/openai-whisper-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; transcription results are written as text or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and OPENAI_API_KEY; sends chosen audio files to OpenAI for transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
