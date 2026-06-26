## Description: <br>
High-performance offline voice pipeline for NVIDIA Jetson with wake word detection, STT, and TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikil511](https://clawhub.ai/user/nikil511) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run a bilingual English/Greek voice assistant pipeline on NVIDIA Jetson-class edge hardware with wake word detection, speech transcription, LLM responses, TTS, LED feedback, and optional Home Assistant control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials and the evidence reports exposed keys. <br>
Mitigation: Rotate or remove exposed keys before installation and provide secrets through environment variables or a secret manager. <br>
Risk: Voice audio and prompts may leave the device through cloud STT, LLM, or TTS services despite offline framing. <br>
Mitigation: Confirm users consent to cloud processing, document which services receive audio or prompts, and use local fallbacks when cloud processing is not acceptable. <br>
Risk: Gateway and Home Assistant integrations can control devices in the user's environment. <br>
Mitigation: Use HTTPS or trusted local-only endpoints and restrict Home Assistant tokens to the minimum devices and actions required. <br>
Risk: Biometric enrollment files are sensitive personal data. <br>
Mitigation: Store enrollment audio and speaker models with restricted permissions and avoid persistent listening in shared spaces without clear consent. <br>


## Reference(s): <br>
- [Voice Pipeline Notes](references/VOICE_PIPELINE_NOTES.md) <br>
- [Groq Audio Transcriptions API](https://api.groq.com/openai/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include systemd, environment variable, audio-device, and Home Assistant configuration guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
