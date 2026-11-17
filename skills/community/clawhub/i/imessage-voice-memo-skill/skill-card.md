## Description:

Send native iMessage voice bubbles with ElevenLabs TTS via BlueBubbles when a user asks to send spoken messages, storytelling, summaries, or other voice-delivered responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amzzzzzzz](https://clawhub.ai/user/amzzzzzzz)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to generate text-to-speech audio, convert it to an iMessage-compatible voice memo format, and send it through a local BlueBubbles server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private message text is sent to ElevenLabs for text-to-speech generation and generated audio is sent through BlueBubbles.

Mitigation: Use the skill only when the user accepts those external service flows, and avoid sending sensitive or regulated content.

Risk: A hard-coded fallback recipient can send voice memos to an unintended phone number if no recipient is supplied.

Mitigation: Remove the fallback recipient and require an explicit recipient plus confirmation before every send.

Risk: The script sources ~/.openclaw/.env directly, which can execute shell content in that file.

Mitigation: Replace direct sourcing with safe key-value parsing for the required environment variables.

Risk: BLUEBUBBLES_URL can be changed to an untrusted endpoint.

Mitigation: Restrict BLUEBUBBLES_URL to a trusted local server or an approved HTTPS endpoint.

## Reference(s):

- [Voice options](references/VOICES.md)
- [ClawHub skill page](https://clawhub.ai/amzzzzzzz/skills/imessage-voice-memo-skill)
- [BlueBubbles](https://bluebubbles.app)
- [ElevenLabs](https://elevenlabs.io)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell command examples and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for sending a voice memo through external ElevenLabs and BlueBubbles services; the shell script creates temporary MP3 and CAF files during execution.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
