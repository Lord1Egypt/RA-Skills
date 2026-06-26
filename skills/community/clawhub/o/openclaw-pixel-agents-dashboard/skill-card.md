## Description: <br>
Real-time pixel art ops dashboard for OpenClaw deployments that visualizes agent activity as character sprites in a shared office with live activity bubbles, hardware monitoring, service controls, and task spawning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaffer1979](https://clawhub.ai/user/jaffer1979) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, configure, run, and troubleshoot a real-time dashboard for monitoring OpenClaw agent sessions, gateway connectivity, hardware status, and task spawning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: If the dashboard server is reachable by untrusted users, unauthenticated controls could restart services, change configuration, run updates, or trigger SSH-related behavior. <br>
Mitigation: Install only in a trusted local environment, bind the dashboard to localhost or place it behind strong authentication, and review the generated configuration before exposing it on any network. <br>
Risk: Remote agent monitoring can introduce SSH credential and remote access risk, especially when password-based SSH is enabled. <br>
Mitigation: Disable remote agents unless needed, prefer SSH key authentication over password-based SSH, and keep secrets in environment variables rather than committed configuration files. <br>
Risk: Service controls and update checks can affect running OpenClaw services. <br>
Mitigation: Disable service-control features that are not required and restrict use to operators who are allowed to manage the local OpenClaw environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jaffer1979/openclaw-pixel-agents-dashboard) <br>
- [README](README.md) <br>
- [Dashboard configuration example](dashboard.config.example.json) <br>
- [Sprite asset license](public/assets/ASSET-LICENSE.md) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct setup scripts to generate dashboard.config.json and may provide troubleshooting steps for local services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
