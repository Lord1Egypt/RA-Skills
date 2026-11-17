## Description:

Use MiniMax speech-2.8-hd model for high-quality text-to-speech synthesis with multiple Chinese and English voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlin53882](https://clawhub.ai/user/jlin53882)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate MP3 speech from text through MiniMax speech-2.8-hd, selecting supported Chinese or English voices and speech speed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user text and the MiniMax API key to the configured MiniMax endpoint.

Mitigation: Use only a trusted MiniMax endpoint, keep MINIMAX_API_KEY scoped and protected, and avoid submitting sensitive text.

Risk: MINIMAX_BASE_URL can redirect requests and credentials to a different endpoint.

Mitigation: Leave MINIMAX_BASE_URL unset unless the endpoint is fully controlled and trusted.

Risk: The package includes an undocumented image-generation and download command in addition to text-to-speech.

Mitigation: Review intended command usage before installation and restrict use to the documented TTS workflow when image generation is not needed.

## Reference(s):

- [MiniMax Platform](https://platform.minimax.io)
- [MiniMax API Base URL](https://api.minimax.io)
- [ClawHub Skill Page](https://clawhub.ai/jlin53882/skills/minimax-tts-voice)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON status output with generated file paths and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MP3 audio files for TTS requests; the artifact also contains an image-generation command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
