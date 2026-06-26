## Description: <br>
小米 TTS Proxy starts a local HTTP proxy that converts OpenAI-compatible TTS requests into Xiaomi MiMo TTS API calls and transcodes audio with FFmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doratiger](https://clawhub.ai/user/doratiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add speech synthesis through a local OpenAI-compatible TTS proxy backed by Xiaomi MiMo TTS. It is also useful when a local service must expose configurable voice presets, style tags, and audio output formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TTS input text is sent to Xiaomi or to the configured upstream proxy. <br>
Mitigation: Use the skill only when that data flow is acceptable for the content being synthesized. <br>
Risk: The Xiaomi API key is stored in ~/.openclaw/tts-proxy.env. <br>
Mitigation: Keep the file private with restrictive permissions such as chmod 600, do not commit or share it, and rotate the key if exposed. <br>
Risk: The optional systemd service can run the proxy in the background. <br>
Mitigation: Review the service definition and environment path before enabling automatic startup. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/doratiger/mimo-tts-proxy) <br>
- [Xiaomi MiMo API Base URL](https://api.xiaomimimo.com) <br>
- [Xiaomi MiMo TTS Endpoint](https://api.xiaomimimo.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code] <br>
**Output Format:** [Markdown with shell commands, JSON configuration, and JavaScript service code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The configured proxy can return opus, mp3, aac, flac, wav, pcm, or pcm16 audio from OpenAI-compatible speech requests.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
