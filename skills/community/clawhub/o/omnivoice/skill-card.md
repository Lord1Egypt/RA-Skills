## Description:

OmniVoice helps agents identify speakers, manage voice references, transcribe audio, clone voices, swap voices, and create persona voice replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangqibin-caibi](https://clawhub.ai/user/yangqibin-caibi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use OmniVoice to process authorized voice or audio inputs for speaker identification, voice library management, transcription, voice cloning, voice swap, and persona voice replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice references, transcripts, and speaker matches can contain biometric and personal data.

Mitigation: Use the skill only with voices the user is authorized to store, identify, clone, or send; keep voice-refs and TOOLS.md private; and define retention for stored references.

Risk: Voice cloning and Feishu sending can share sensitive audio data and credentials with external services.

Mitigation: Treat SiliconFlow and Feishu calls as external sharing, review recipients before sending, scope credentials tightly, and avoid broad automatic activation.

Risk: Speaker identification can be inaccurate, especially for short or similar-sounding same-gender samples.

Mitigation: Use clear authorized reference audio, adjust thresholds for stricter matching, and require human review before taking consequential action from an identification result.

## Reference(s):

- [Voice Library Format](references/voice-library-format.md)
- [ClawHub skill page](https://clawhub.ai/yangqibin-caibi/skills/omnivoice)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, audio files]

**Output Format:** [Markdown guidance with inline shell commands and generated audio file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local audio tools, download speaker-identification models, use SiliconFlow for voice cloning, and send audio through Feishu when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
