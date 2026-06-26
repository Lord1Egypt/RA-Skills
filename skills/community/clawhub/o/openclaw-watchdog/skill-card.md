## Description: <br>
Self-healing monitoring system for the OpenClaw gateway that auto-detects failures, fixes crashes, and sends Telegram alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdullah4AI](https://clawhub.ai/user/Abdullah4AI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install and manage a background watchdog that monitors gateway health, attempts recovery, and sends Telegram alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an always-on user-level background service. <br>
Mitigation: Review service installation details before setup and use the documented LaunchAgent or systemd uninstall steps when the watchdog is no longer needed. <br>
Risk: The skill handles Telegram credentials and sends operational diagnostics to Telegram. <br>
Mitigation: Use a dedicated Telegram bot token, avoid pasting it into persistent chat or shell history, and rotate the token if it may have been exposed. <br>
Risk: The watchdog can restart the OpenClaw gateway and perform high-impact recovery actions. <br>
Mitigation: Understand the recovery behavior before enabling it; OpenClaw reinstall is gated by a local approval marker file. <br>
Risk: The security verdict is suspicious due to persistence, secret handling, external notifications, and weak safeguards around recovery behavior. <br>
Mitigation: Review carefully before installing and do not provide OpenAI or Anthropic keys unless a later version clearly requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Abdullah4AI/openclaw-watchdog) <br>
- [Publisher profile](https://clawhub.ai/user/Abdullah4AI) <br>
- [Watch Dog Troubleshooting](references/troubleshooting.md) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, credential validation, service verification, troubleshooting, and uninstall guidance.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
