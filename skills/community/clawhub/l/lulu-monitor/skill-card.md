## Description: <br>
LuLu Monitor is an AI-powered LuLu Firewall companion for macOS that monitors firewall alerts, analyzes connections, and sends Telegram notifications with Allow/Block actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and macOS operators use this skill to install, configure, and troubleshoot a LuLu Firewall monitor that forwards connection alerts to Telegram and can apply selected firewall actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer creates a persistent LaunchAgent and installs unpinned remote code. <br>
Mitigation: Review the repository and npm dependencies before installation, and remove the LaunchAgent when the monitor is no longer needed. <br>
Risk: AI-driven or auto-executed actions can change firewall rules. <br>
Mitigation: Keep auto-execute disabled unless automatic firewall changes are acceptable, and prefer temporary allow/block actions over permanent rules. <br>
Risk: The monitor depends on macOS Accessibility permission to control LuLu. <br>
Mitigation: Grant Accessibility only to the required terminal or automation process, and revoke it when the monitor is no longer in use. <br>


## Reference(s): <br>
- [LuLu Firewall](https://objective-see.org/products/lulu.html) <br>
- [OpenClaw Telegram Channel Documentation](https://docs.openclaw.ai/channels/telegram) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, JSON, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operator-facing setup, callback-handling, and troubleshooting instructions for macOS, LuLu Firewall, OpenClaw Gateway, and Telegram.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
