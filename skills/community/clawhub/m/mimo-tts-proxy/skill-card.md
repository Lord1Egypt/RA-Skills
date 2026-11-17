## Description:

Xiaomi TTS Proxy runs a local OpenAI-compatible TTS proxy that forwards speech requests to Xiaomi's MIMO TTS API and transcodes returned audio with FFmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[doratiger](https://clawhub.ai/user/doratiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to configure local text-to-speech for bots or services through an OpenAI-compatible endpoint backed by Xiaomi MIMO TTS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The proxy sends TTS input text and the Xiaomi API key to a configurable upstream endpoint.

Mitigation: Use only a trusted HTTPS MIMO_TTS_BASE, avoid sending sensitive text, and protect and rotate the Xiaomi API key.

Risk: The setup recommends a persistent systemd service that may run continuously on the host.

Mitigation: Review the service unit and file permissions before enabling the service, and enable persistence only after that review.

Risk: Audio conversion depends on FFmpeg and local temporary files.

Mitigation: Install FFmpeg from a trusted source and review host file permissions for the temporary working directory before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/doratiger/skills/mimo-tts-proxy)
- [Publisher profile](https://clawhub.ai/user/doratiger)
- [Xiaomi MIMO API base](https://api.xiaomimimo.com)
- [Xiaomi MIMO chat completions endpoint used by the proxy](https://api.xiaomimimo.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and Node.js proxy code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides setup of a local HTTP TTS proxy and supported audio response formats: opus, mp3, aac, flac, wav, pcm, and pcm16.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
