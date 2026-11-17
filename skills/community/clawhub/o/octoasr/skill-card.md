## Description:

OctoASR helps configure OpenClaw to transcribe incoming audio messages locally on Apple Silicon Macs and inject the resulting text into conversation context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovejing0306](https://clawhub.ai/user/lovejing0306)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up offline speech-to-text for OpenClaw deployments on Apple Silicon Macs. It is intended for workflows where audio messages from channels such as Telegram, Discord, Signal, WebChat, or enterprise chat need to become text before agent processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from the OctoASR Homebrew tap requires trusting that third-party distribution source.

Mitigation: Review and approve the Homebrew tap and package source before installing in managed environments.

Risk: Using the optional OpenAI fallback may send audio or transcription requests to an external provider when local transcription fails.

Mitigation: Use the local-only configuration for private or enterprise audio unless external processing has been approved.

## Reference(s):

- [OctoASR project](https://github.com/Mininglamp-AI/octoasr)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [Homebrew](https://brew.sh)
- [ClawHub skill page](https://clawhub.ai/lovejing0306/skills/octoasr)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guide with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local transcription setup, service management, model selection, troubleshooting, and optional cloud fallback configuration.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
