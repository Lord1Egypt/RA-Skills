## Description:

Transcribe audio via OpenAI Audio Transcriptions API (Whisper).

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe local audio files through OpenAI's Audio Transcriptions API using a curl-based wrapper. It is useful for producing transcript text or JSON while keeping API key handling and common transcription options in one workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can unintentionally upload local files when prompt, model, or language values begin with curl multipart metacharacters.

Mitigation: Change non-file multipart fields to curl --form-string and avoid untrusted prompt, model, or language values until that hardening is complete.

Risk: The skill depends on an OpenAI API key and may expose credentials if debugging or setup commands reveal environment variables or credential files.

Mitigation: Verify credential presence without printing secret values and do not display, encode, transmit, or read credential-containing files.

Risk: Audio files may contain sensitive data and are sent to an external transcription API.

Mitigation: Confirm the user intends to upload the selected audio file and follow the deployment's data handling requirements before transcription.

## Reference(s):

- [OpenAI Speech-to-Text Documentation](https://platform.openai.com/docs/guides/speech-to-text)
- [OpenAI Audio Transcriptions Endpoint](https://api.openai.com/v1/audio/transcriptions)
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/openai-whisper-api-hardened)
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/openai-whisper-api)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; the script writes text or JSON transcript files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and OPENAI_API_KEY. Default model is whisper-1; optional flags include output path, language, prompt, and JSON response format.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
