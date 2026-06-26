## Description: <br>
OpenClaw Gateway watchdog that monitors process health, WebSocket errors, Feishu, WeCom, Weixin channel state, and network connectivity, then restarts Gateway within configured limits and records paused-channel state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxwseeyouaska](https://clawhub.ai/user/lxwseeyouaska) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run or deploy a watchdog for OpenClaw Gateway availability, channel error detection, and bounded automatic recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog can automatically restart OpenClaw Gateway in the background. <br>
Mitigation: Review the restart policy before deployment and tune MAX_RESTARTS, RESTART_WINDOW, and the systemd restart settings for the target environment. <br>
Risk: Network-error handling can make persistent host proxy changes. <br>
Mitigation: In managed or proxy-dependent environments, review or remove disable_proxy before installation, especially the /etc/profile.d move, systemd environment clearing, and ~/.bashrc edit. <br>
Risk: Channel sessions or platform limits may require manual recovery. <br>
Mitigation: Monitor the generated pause-state files and logs, and refresh Feishu or WeCom authorization manually when token or session expiry is reported. <br>


## Reference(s): <br>
- [OpenClaw Watchdog Li on ClawHub](https://clawhub.ai/lxwseeyouaska/openclaw-watchdog-liwg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Bash and systemd snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment-variable configuration for watchdog interval, log paths, restart limits, restart window, and OpenClaw Gateway port.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
