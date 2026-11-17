## Description:

Text-to-speech (TTS) generation using the MiniMax API converts text into natural-sounding speech with multiple voices, adjustable speed and pitch, and MP3, WAV, or PCM output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanhaixuan](https://clawhub.ai/user/lanhaixuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to convert text, scripts, articles, and multi-segment narration into speech audio through the MiniMax API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send submitted text and the MiniMax API key to an arbitrary API host when MINIMAX_API_HOST is set.

Mitigation: Run only in a trusted environment, leave MINIMAX_API_HOST unset unless the endpoint is fully trusted, and use a dedicated low-quota API key.

Risk: Generated speech requests may disclose sensitive text to MiniMax or to the configured endpoint.

Mitigation: Review text before generation and avoid submitting confidential, regulated, or third-party data unless the destination and account terms permit it.

Risk: The server security verdict is suspicious because the endpoint override can redirect requests.

Mitigation: Review the skill before installing, rotate keys after any unexpected host override, and monitor API usage for anomalous requests.

## Reference(s):

- [MiniMax Open Platform](https://platform.minimaxi.com)
- [MiniMax Speech Synthesis Product](https://www.minimaxi.com/models/speech)
- [ClawHub Skill Page](https://clawhub.ai/lanhaixuan/skills/minimax-tts-generator)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, files, JSON]

**Output Format:** [JSON status responses and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MP3, WAV, or PCM audio files; generated text may be sent to MiniMax or to the endpoint configured by MINIMAX_API_HOST.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
