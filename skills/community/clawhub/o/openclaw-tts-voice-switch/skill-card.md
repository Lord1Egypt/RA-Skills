## Description:

Switch OpenClaw ElevenLabs TTS voices by updating ~/.openclaw/openclaw.json, keeping Chinese-safe defaults, and restarting the gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nowloady](https://clawhub.ai/user/nowloady)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to list ElevenLabs voices, switch the Gateway built-in TTS voice, and keep language and model settings aligned with the target voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read or modify ~/.openclaw/openclaw.json and restart the OpenClaw gateway.

Mitigation: Review intended configuration changes before running the scripts, keep the generated backup, and verify Gateway behavior after restart.

Risk: The documented apiKey command-line argument can expose an ElevenLabs API key through shell history or process visibility.

Mitigation: Do not pass the API key as a command-line argument; rely on an already protected config value or a safer secret-entry method, and rotate any key that was exposed.

## Reference(s):

- [TTS Parameters](references/tts-parameters.md)
- [ElevenLabs Voices API](https://api.elevenlabs.io/v1/voices)
- [ClawHub Skill Page](https://clawhub.ai/nowloady/skills/openclaw-tts-voice-switch)
- [Publisher Profile](https://clawhub.ai/user/nowloady)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update ~/.openclaw/openclaw.json and restart the OpenClaw gateway when the provided scripts are run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
