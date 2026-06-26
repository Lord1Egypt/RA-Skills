## Description: <br>
Provides a web interface to monitor OpenClaw nodes, manage agent configurations, oversee resource usage and security policies, and review system logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wufan2026](https://clawhub.ai/user/wufan2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators administering OpenClaw Gateway use this skill to monitor nodes, manage agents, sessions, models, channels, skills, and inspect resource usage and logs from a centralized dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard exposes powerful host and OpenClaw Gateway controls. <br>
Mitigation: Install only in a trusted local or tightly firewalled admin environment and limit access to trusted operators. <br>
Risk: Weak default scoping and under-protected endpoints may expose administrative actions. <br>
Mitigation: Configure strong AUTH_USERNAME and AUTH_PASSWORD before exposure, review unauthenticated npm update and media endpoints, and avoid public internet deployment. <br>
Risk: Dashboard users may be able to control the host and access secrets, backups, or OpenClaw state. <br>
Mitigation: Treat dashboard access as privileged administrative access and rotate or revoke credentials after suspected exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wufan2026/openclaw-admin-main) <br>
- [OpenClaw releases](https://github.com/openclaw/openclaw/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Vue and TypeScript project files with Markdown setup and operating guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a browser-based admin dashboard and Node.js server for OpenClaw Gateway management.] <br>

## Skill Version(s): <br>
0.2.8 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
