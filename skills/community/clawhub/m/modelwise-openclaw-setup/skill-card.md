## Description: <br>
Guides agents through installing, configuring, and troubleshooting OpenClaw gateways across Windows, macOS, and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deerleo](https://clawhub.ai/user/deerleo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up OpenClaw, configure model-provider credentials and messaging channels, start the gateway, and run basic diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copyable gateway examples can expose OpenClaw beyond the local machine. <br>
Mitigation: Prefer binding the gateway to 127.0.0.1 unless LAN access is intentional, and keep token authentication enabled. <br>
Risk: Telegram examples can allow broad access when open direct-message policy or wildcard allowlists are used. <br>
Mitigation: Use pairing mode or explicit allowlists for private bots and review group activation settings before deployment. <br>
Risk: Setup commands involve API keys and bot tokens that may be visible in terminals or shell history. <br>
Mitigation: Avoid printing secrets in shared terminals and store credentials through OpenClaw credential commands or environment-backed configuration. <br>
Risk: Reset and stop commands can delete local OpenClaw configuration or terminate running Node processes. <br>
Mitigation: Back up configuration before reset operations and inspect target processes before force-stopping them. <br>
Risk: The artifact includes a ClawHub publishing helper unrelated to installing OpenClaw. <br>
Mitigation: Do not run publish.sh unless the intent is specifically to publish a ClawHub skill. <br>


## Reference(s): <br>
- [OpenClaw Website](https://openclaw.ai) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [Configuration Reference](references/configuration-reference.md) <br>
- [Telegram Setup Guide](examples/telegram-setup.md) <br>
- [Example OpenClaw Configuration](examples/openclaw.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform-specific command variants for Windows, macOS, and Linux.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
