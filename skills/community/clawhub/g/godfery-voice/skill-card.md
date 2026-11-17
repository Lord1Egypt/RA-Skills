## Description:

Enables real-time voice chat in Discord channels with speech-to-text, Claude AI processing, and text-to-speech playback supporting barge-in and auto-reconnect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Discord bot operators use this skill to add real-time voice conversations to an OpenClaw or Clawdbot agent, routing Discord speech through STT, the agent, and TTS playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discord voice participants may send prompts to the main agent through the voice channel.

Mitigation: Install only after deciding that this access is acceptable and configure allowedUsers or other channel controls before deployment.

Risk: Provider credentials and conversation data may be exposed to external STT, TTS, or SkillBoss/HeyBossAI processing.

Mitigation: Use plugin-specific, revocable, capped credentials, verify provider data handling before use, and prefer local or offline providers for sensitive conversations.

Risk: Production deployments depend on a dependency lockfile and voice/audio dependencies that may change over time.

Mitigation: Review or update the dependency lockfile and required system dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/godfery-voice)
- [Complete setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [Text, Audio, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with configuration and command examples; runtime output includes Discord voice audio and status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable STT and TTS providers, voice activity detection, barge-in, auto-reconnect, and optional local/offline providers.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; target metadata version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
