## Description:

Simple text-to-speech skill using MiniMax Voice API. Converts text to audio with customizable voice selection. Use for generating speech audio from text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blue-coconut](https://clawhub.ai/user/blue-coconut)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to generate speech audio from text with MiniMax voices, including segment-based multi-voice workflows, custom voice cloning or design, and FFmpeg-based audio merging/conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TTS text and selected voice samples may be uploaded to MiniMax during synthesis, async TTS, voice cloning, or voice design.

Mitigation: Use the skill only with content approved for MiniMax processing, avoid regulated or confidential input unless authorized, and clone only voices the operator has permission to use.

Risk: The MiniMax API endpoint can be redirected through MINIMAX_API_BASE, which could expose API keys and content to another host.

Mitigation: Keep MINIMAX_API_BASE unset or explicitly pinned to the official MiniMax origin before running the skill, and use a least-privilege API key.

Risk: Voice deletion helpers can remove custom cloned or designed voices from the connected MiniMax account.

Mitigation: Review any workflow that calls custom-voice deletion functions before allowing autonomous execution.

## Reference(s):

- [Skill page](https://clawhub.ai/blue-coconut/skills/mm-easy-voice)
- [Getting Started](reference/getting-started.md)
- [Audio Processing Guide](reference/audio-guide.md)
- [Voice Management Guide](reference/voice-guide.md)
- [Troubleshooting](reference/troubleshooting.md)
- [MiniMax Voice Catalog](reference/voice_catalog.md)
- [MiniMax async TTS create API](https://platform.minimaxi.com/docs/api-reference/speech-t2a-async-create)
- [MiniMax async TTS query API](https://platform.minimaxi.com/docs/api-reference/speech-t2a-async-query)
- [MiniMax voice cloning upload API](https://platform.minimaxi.com/docs/api-reference/voice-cloning-uploadcloneaudio)
- [MiniMax voice cloning API](https://platform.minimaxi.com/docs/api-reference/voice-cloning-clone)
- [MiniMax voice management API](https://platform.minimaxi.com/docs/api-reference/voice-management-get)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and Python CLI/API usage; generated workflows may write audio files such as MP3, WAV, FLAC, or PCM.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax voice API key; FFmpeg is optional for merge, conversion, and audio processing workflows.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
