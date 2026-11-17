## Description:

Local macOS voice-control integration for OpenClaw. Use when setting up, deploying, troubleshooting, or operating wakeword-triggered voice access to a local OpenClaw agent with ASR, TTS, overlay UI, and launchd background support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carrotyuan](https://clawhub.ai/user/carrotyuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up, validate, troubleshoot, and manage a local macOS voice-control path for an OpenClaw agent, including wakeword activation, ASR, TTS, overlay UI, and optional launchd background behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to download and run mutable GitHub code and deployment scripts with sensitive local access.

Mitigation: Install only after reviewing or pinning the exact repository commit and deployment scripts, and avoid launchd auto-start until the background behavior is understood.

Risk: Microphone access and OPENCLAW_TOKEN create sensitive local authority, and voice-triggered requests may reach capabilities exposed by the connected OpenClaw agent.

Mitigation: Use a least-privilege OpenClaw agent, require confirmations for risky voice-triggered actions, and treat microphone access plus OPENCLAW_TOKEN as sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carrotyuan/skills/openclaw-voice-control)
- [OpenClaw Voice Control homepage](https://github.com/CarrotYuan/openclaw-voice-control)
- [Picovoice](https://picovoice.ai/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets macOS setup and operation; requires local OpenClaw, microphone permission, Python, git, launchctl, model paths, and an OpenClaw token.]

## Skill Version(s):

0.1.9 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
