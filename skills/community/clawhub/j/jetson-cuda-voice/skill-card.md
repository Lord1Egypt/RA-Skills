## Description:

High-performance bilingual voice assistant pipeline for NVIDIA Jetson with wake word detection, speech transcription, spoken responses, and Home Assistant control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikil511](https://clawhub.ai/user/nikil511)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and run a bilingual voice assistant on NVIDIA Jetson hardware for wake-word interactions, STT, LLM responses, TTS, and smart-home device control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-listening microphone and cloud-processing behavior may be inappropriate for some environments.

Mitigation: Enable the service only where continuous microphone capture and the documented cloud data flows have been reviewed and accepted.

Risk: Voice data and assistant requests may be sent to external cloud services.

Mitigation: Review provider data flows before deployment and require user-provided API keys rather than bundled or shared credentials.

Risk: Home Assistant control can affect real devices.

Mitigation: Use HTTPS or localhost-only endpoints with least-privilege Home Assistant tokens and limit exposed actions to intended devices.

Risk: Credential and authentication weaknesses are identified in the security evidence.

Mitigation: Rotate any embedded credentials, remove secrets from source files, and load secrets through the deployment environment.

Risk: Speaker verification and serialized model loading can fail open or load unsafe files if deployed carelessly.

Mitigation: Make speaker verification fail closed and avoid loading joblib or pickle files from untrusted writable paths.

## Reference(s):

- [Greek Voice Assistant Pipeline - Implementation Status](references/VOICE_PIPELINE_NOTES.md)
- [Groq Audio Transcriptions API](https://api.groq.com/openai/v1/audio/transcriptions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment variable names, service commands, device paths, and implementation guidance for a Jetson voice pipeline.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
