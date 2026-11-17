## Description:

Moark Tts helps agents generate speech and extract CosyVoice voice features through Gitee AI TTS models while collecting only the parameters relevant to the selected model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fchange](https://clawhub.ai/user/fchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workflow users use this skill to synthesize speech with one of fifteen Gitee AI TTS model choices or prepare CosyVoice voice features for cloning workflows. It is suited to agents that need model-specific parameter guidance and a direct script-based execution path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accepts user-supplied reference audio URLs, which can create risk when URLs point to internal, local, metadata, or private-network resources.

Mitigation: Review URLs before execution and prefer a patched version that validates allowed schemes and destinations, limits downloaded file size and type, and blocks private-network targets.

Risk: The skill uses a Gitee AI API key from the agent environment or command line.

Mitigation: Use only a Gitee AI key approved for the agent environment, avoid exposing secrets in prompts or logs, and send the key only to trusted Gitee AI endpoints.

Risk: Voice samples and generated voice features can involve third-party biometric or personal data.

Mitigation: Use reference audio only with consent and avoid submitting sensitive or third-party voice samples unless the workflow has appropriate authorization.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fchange/skills/moark-tts)
- [TTS Model Routing](artifact/references/models.md)
- [Gitee AI API Base](https://ai.gitee.com/v1)
- [Gitee AI Voice Feature Extraction Endpoint](https://ai.gitee.com/v1/audio/voice-feature-extraction)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown-style agent responses with command guidance, script output labels, URLs, and optional generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITEEAI_API_KEY; speech output may be returned as AUDIO_URL, AUDIO_FILE, or TTS_RESULT, and voice-feature output may be returned as VOICE_URL or VOICE_FEATURE_FILE.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
