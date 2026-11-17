## Description:

Convert text to speech using the MiniMax API and prepare Feishu voice-bubble replies when a user asks for a voice response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronjager92](https://clawhub.ai/user/aaronjager92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu automation maintainers use this skill to convert triggered text replies into MiniMax-generated OGG/Opus audio that can be sent as Feishu voice bubbles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice-reply text is sent to the MiniMax TTS service.

Mitigation: Avoid sensitive or confidential content and use explicit trigger phrases or confirmation before sending text for speech generation.

Risk: An unsafe output path can overwrite or delete writable files during audio conversion and cleanup.

Mitigation: Restrict generated audio paths to the OpenClaw workspace and validate or sanitize output paths before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaronjager92/skills/minimax-voicereponse-feishu)
- [MiniMax Platform](https://www.minimaxi.com/)
- [Artifact README](references/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python script execution output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime script prints the generated OGG audio file path after converting MiniMax TTS output for Feishu compatibility.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
