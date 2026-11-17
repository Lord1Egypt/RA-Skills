## Description:

Generates Chinese text-to-speech audio with edge-tts and guides agents to send the resulting voice files through channels such as Feishu, Telegram, and Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binbin1213](https://clawhub.ai/user/binbin1213)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to convert Chinese text into voice-message audio and send it through supported chat channels. It is suited for notifications, customer replies, announcements, and segmented long-form voice messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for synthesis is sent through edge-tts and may contain sensitive or regulated information.

Mitigation: Avoid secrets and regulated data in TTS text, and review content before generating audio.

Risk: The skill depends on the external edge-tts package and service.

Mitigation: Install edge-tts only after review, prefer pipx with a pinned version, and use the skill only when that dependency is acceptable.

Risk: Generated audio files are written locally and can be sent to external chat destinations.

Mitigation: Use the default output location when possible, clean up generated files after use, and verify the destination before sending audio.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binbin1213/skills/ms-voice-tts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and JSON message payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Opus audio file paths that can be passed to supported messaging channels.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
