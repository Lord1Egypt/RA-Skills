## Description: <br>
Real-time speech-to-text streaming with Gladia via WebSocket for live transcription, voice agents, meeting recorders, call center integrations, live subtitles, and other low-latency audio streaming applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gladiaio](https://clawhub.ai/user/gladiaio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Gladia live transcription sessions, stream audio over the official SDK or WebSocket fallback, tune latency and language settings, and manage live session results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live audio and transcripts may contain sensitive participant data. <br>
Mitigation: Obtain required consent before streaming or recording audio, minimize enabled analytics features, and delete retained sessions when they are no longer needed. <br>
Risk: The skill requires a Gladia API key. <br>
Mitigation: Store the API key in a secure secret manager or environment variable and avoid placing credentials in code, logs, transcripts, or shared prompts. <br>
Risk: Callback URLs can expose live session events to external systems. <br>
Mitigation: Use callback URLs only for trusted HTTPS endpoints that are authorized to receive transcription events. <br>
Risk: Incorrect language or audio format settings can produce unreliable transcripts. <br>
Mitigation: Match encoding, sample rate, bit depth, and channel count to the audio stream, and configure expected languages before starting a session. <br>


## Reference(s): <br>
- [Recommended Parameters by Use Case](references/recommended-params.md) <br>
- [Session Configuration Reference](references/session-config.md) <br>
- [Managing Live Sessions](references/managing-sessions.md) <br>
- [WebSocket Message Types](references/websocket-events.md) <br>
- [Gladia live quickstart](https://docs.gladia.io/chapters/live-stt/quickstart) <br>
- [Gladia partial transcripts](https://docs.gladia.io/chapters/live-stt/features/partial-transcripts) <br>
- [Gladia endpointing](https://docs.gladia.io/chapters/live-stt/features/endpointing) <br>
- [Gladia live init API reference](https://docs.gladia.io/api-reference/v2/live/init) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration, Shell commands] <br>
**Output Format:** [Markdown with inline TypeScript, Python, JSON, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include SDK-first implementation guidance, session configuration values, WebSocket event handling patterns, and session management steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
