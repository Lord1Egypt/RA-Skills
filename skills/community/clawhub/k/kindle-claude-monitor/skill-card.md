## Description: <br>
Turns a Kindle, phone, tablet, or secondary browser screen into a Claude Code status monitor that shows hook-driven states such as thinking, running tools, waiting for confirmation, and done. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heavenchenggong](https://clawhub.ai/user/heavenchenggong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers who use Claude Code can use this skill to route local hook events into a browser-readable status dashboard for a nearby Kindle or spare screen, so they can notice tool activity and confirmation waits without watching the terminal continuously. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local monitor can expose Claude Code workflow data to devices that can reach the monitor port on the local network. <br>
Mitigation: Install only on a trusted private network and limit network access to devices that should see Claude Code status data. <br>
Risk: The skill installs persistent Claude Code hooks and a launchd service that can log hook activity locally. <br>
Mitigation: Review hook changes and the service before installation, and remove them with the uninstall script when monitoring is no longer needed. <br>
Risk: Changing firewall settings to make the dashboard reachable can increase local network exposure. <br>
Mitigation: Avoid disabling firewall protections unless necessary, and prefer a restricted trusted network when using a secondary display. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/heavenchenggong/kindle-claude-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, operation, troubleshooting, and uninstall guidance for a local status dashboard.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
