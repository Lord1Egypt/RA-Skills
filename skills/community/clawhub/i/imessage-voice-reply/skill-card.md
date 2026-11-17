## Description:

iMessage Voice Reply generates local Kokoro-ONNX TTS audio and sends it through BlueBubbles as native iMessage voice bubbles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bolander72](https://clawhub.ai/user/bolander72)

### License/Terms of Use:


## Use Case:

OpenClaw users use this skill to reply with audio when a user sends a voice message or explicitly asks for a voice response. It helps an agent generate local TTS audio, prepare it in an iMessage-friendly format, and send it through a configured BlueBubbles channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs Python packages and caches Kokoro model files locally.

Mitigation: Review or pin dependencies before installation and run setup in the skill's isolated virtual environment.

Risk: Temporary text or audio files may contain message content.

Mitigation: Use private mktemp-created directories for sensitive replies and remove temporary text and audio files after use.

Risk: The skill can send generated audio as an iMessage attachment through BlueBubbles.

Mitigation: Review the recipient target and required voice-message parameters before sending, and include a text reply for accessibility.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bolander72/skills/imessage-voice-reply)
- [ClawHub publisher profile](https://clawhub.ai/user/bolander72)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local audio generation commands and BlueBubbles attachment parameters for agent use.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
