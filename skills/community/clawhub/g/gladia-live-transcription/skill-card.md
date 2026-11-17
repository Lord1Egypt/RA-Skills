## Description:

Guides developers in configuring Gladia live audio streaming for low-latency partial and final speech transcripts, using the official SDK where possible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gladiaio](https://clawhub.ai/user/gladiaio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build live transcription for voice agents, meetings, call centers, and captions, including session configuration, audio streaming, and transcript event handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live audio and transcripts can contain sensitive or confidential information sent to Gladia.

Mitigation: Obtain appropriate consent and choose retention and deletion settings before processing conversations.

Risk: Configured callbacks may expose conversation data to another endpoint.

Mitigation: Secure callback receivers and send data only to approved endpoints.

Risk: Deleting a session can remove its associated recording and results.

Mitigation: Require explicit confirmation before deleting sessions or recorded files.

## Reference(s):

- [Gladia Live Transcription on ClawHub](https://clawhub.ai/gladiaio/skills/gladia-live-transcription)
- [Gladia live transcription quickstart](https://docs.gladia.io/chapters/live-stt/quickstart)
- [Gladia live session API reference](https://docs.gladia.io/api-reference/v2/live/init)
- [Session configuration reference](references/session-config.md)
- [WebSocket events reference](references/websocket-events.md)
- [Managing sessions reference](references/managing-sessions.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions]

**Output Format:** [Markdown with JavaScript/TypeScript and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers partial and final transcripts, session lifecycle, and optional post-processing.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
