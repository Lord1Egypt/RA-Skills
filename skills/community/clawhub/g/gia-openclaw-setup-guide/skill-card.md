## Description: <br>
Guides users through installing OpenClaw, connecting messaging channels, configuring skills, setting up workflows, and troubleshooting common setup issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merjua14](https://clawhub.ai/user/merjua14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide first-time OpenClaw setup, including local installation, onboarding, channel connections, identity files, skill installation, automation workflows, and common troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow includes a remote shell installer. <br>
Mitigation: Review or separately download the installer before running it instead of blindly piping it to bash. <br>
Risk: Messaging channel setup can expose Telegram or Discord bot tokens. <br>
Mitigation: Provide only tokens intended for OpenClaw and rotate or revoke them if they are exposed. <br>
Risk: Optional daemon, cron, heartbeat, and memory settings can make the agent persistent and retain context. <br>
Mitigation: Enable persistent automation and memory files only when that ongoing behavior is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/merjua14/gia-openclaw-setup-guide) <br>
- [Publisher profile](https://clawhub.ai/user/merjua14) <br>
- [OpenClaw installer](https://openclaw.ai/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and setup checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include channel setup steps, token-handling reminders, troubleshooting guidance, and workflow examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
