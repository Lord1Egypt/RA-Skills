## Description:

Self-healing monitoring system for OpenClaw gateway that auto-detects failures, fixes crashes, and sends Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdullah4ai](https://clawhub.ai/user/abdullah4ai)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to install and operate a local watchdog service that monitors gateway health, restarts the gateway after repeated failures, and sends Telegram alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent user-level watchdog service that can restart the OpenClaw gateway and send Telegram alerts.

Mitigation: Install it only when persistent gateway monitoring and automatic recovery are intended, and verify the installed service status and logs after setup.

Risk: Sensitive Telegram credentials, and optional unused API keys if supplied, may be retained by the installed service configuration.

Mitigation: Provide only the required Telegram token and chat ID, avoid supplying OpenAI or Anthropic API keys, and rotate the Telegram bot token if it may have appeared in logs.

Risk: The security scan notes unpinned aiohttp and npm openclaw install behavior.

Mitigation: Review package installation behavior before enabling automatic recovery, and pin or approve dependency sources according to local deployment policy.

## Reference(s):

- [OpenClaw Watch Dog ClawHub listing](https://clawhub.ai/abdullah4ai/skills/openclaw-watchdog)
- [Publisher profile](https://clawhub.ai/user/abdullah4ai)
- [Watch Dog Troubleshooting](artifact/openclaw-watchdog/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command snippets and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, openssl, TELEGRAM_TOKEN, and TELEGRAM_CHAT_ID; installs a user-level LaunchAgent or systemd service.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
