## Description:

Interactive setup wizard that wires the OpenClaw Prediction Market Trading Stack into a connected system by detecting installed skills, configuring API keys, creating scheduled scans and alerts, enabling heartbeat, setting up iMessage delivery, and testing the pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingmadellc](https://clawhub.ai/user/kingmadellc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and prediction-market operators use this skill to configure the OpenClaw prediction-market stack, validate required APIs, set up local credentials, create scheduled scans, and route alerts through iMessage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses trading API credentials and private keys in local OpenClaw configuration.

Mitigation: Set ~/.openclaw to 0700 and set ~/.openclaw/config.yaml plus private key files to 0600 before running validation or scheduled jobs.

Risk: Troubleshooting commands can print API keys, private-key material, or environment variables into a shared or logged terminal.

Mitigation: Avoid commands that display secrets, redact terminal output before sharing it, and rotate any credential that has already been displayed.

Risk: The setup creates persistent cron jobs for market scanning, position monitoring, and iMessage alerts.

Mitigation: Review each cron job, delivery target, alert threshold, and timeout before adding it, then use the validation script and cron list command to confirm the intended schedule.

Risk: The configured stack can produce trading-related alerts and recommendations that may be incomplete or wrong.

Mitigation: Treat outputs as decision support, validate required services before relying on alerts, and review trade decisions independently before execution.

## Reference(s):

- [Prediction Stack Setup README](README.md)
- [API Validation Troubleshooting Guide](references/validation-troubleshooting.md)
- [Configuration Template](config.example.yaml)
- [OpenClaw Prediction Market Trading Stack](https://github.com/kingmadellc/openclaw-prediction-stack)
- [Kalshi API Keys](https://kalshi.com/settings/api)
- [Anthropic API Keys](https://console.anthropic.com/account/keys)
- [BlueBubbles](https://bluebubbles.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or update local OpenClaw configuration and scheduled jobs when the user follows the commands.]

## Skill Version(s):

1.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
