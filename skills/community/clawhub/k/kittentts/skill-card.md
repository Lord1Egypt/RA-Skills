## Description:

Generate local text-to-speech audio using the KittenTTS model with selectable voices and multiple model sizes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fredguile](https://clawhub.ai/user/fredguile)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to generate local TTS audio files with KittenTTS and selectable voices, including workflows where OpenClaw sends generated audio through Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a remote wheel and dependencies without verification can introduce supply-chain risk.

Mitigation: Install in an isolated virtual environment, verify the KittenTTS release source, and pin dependency versions and hashes where practical.

Risk: Text converted to speech through the Telegram integration may be transmitted externally.

Mitigation: Avoid processing sensitive text through Telegram unless external audio transmission is intended and approved.

## Reference(s):

- [ClawHub Kittentts skill page](https://clawhub.ai/fredguile/skills/kittentts)
- [KittenTTS 0.8.1 release wheel](https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, audio files]

**Output Format:** [Markdown with bash and Python code blocks; generated WAV audio when the commands are executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice and model size are configurable; Telegram delivery depends on the OpenClaw integration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
