## Description:

Send voice messages to Feishu using NoizAI TTS. Use this whenever the user wants you to speak, send a voice message, or reply with audio on Feishu. Wraps noizai-tts + Feishu voice delivery into one reliable workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lubo1012](https://clawhub.ai/user/lubo1012)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate NoizAI opus voice audio and send it as a Feishu voice message instead of a file attachment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spoken text is sent to NoizAI and generated audio is sent to Feishu.

Mitigation: Avoid sensitive content unless the NoizAI dependency version, account mode, and data-handling behavior are clear.

Risk: The workflow depends on the external noizai-tts skill.

Mitigation: Install only after reviewing and trusting the noizai-tts dependency used in the environment.

Risk: Generated voice files are saved locally before Feishu delivery.

Mitigation: Review storage location and retention practices for generated .opus files when handling private messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lubo1012/skills/lubo-feishu-voice)
- [Publisher profile](https://clawhub.ai/user/lubo1012)
- [NoizAI TTS endpoint](https://noiz.ai/v1/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local .opus audio files for Feishu voice delivery; stdout prints the generated file path.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
