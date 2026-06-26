## Description: <br>
Openclaw Chat provides a mobile and PWA interface for OpenClaw multi-agent chat, group management, service status controls, scheduled tasks, logs, and recovery-oriented admin actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsun4414](https://clawhub.ai/user/johnsun4414) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install and run a mobile-friendly chat and administration panel for monitoring agents, groups, services, cron jobs, logs, and recovery workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact appears to be a frontend/mobile admin panel with service controls and recovery actions that could affect local OpenClaw services if connected to real backends. <br>
Mitigation: Run it only on trusted local networks and add authentication, explicit confirmations, and clear data-retention rules before wiring controls to real services or memory sync. <br>
Risk: The artifact advertises emergency recovery and self-healing behavior, but security evidence characterizes those controls as mostly simulated rather than proven recovery automation. <br>
Mitigation: Treat recovery actions as operator-facing UI until integrated and tested against real OpenClaw service APIs. <br>


## Reference(s): <br>
- [Openclaw Chat on ClawHub](https://clawhub.ai/johnsun4414/openclaw-chat) <br>
- [Artifact Skill README](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, TypeScript/React application code, shell commands, and mobile/PWA configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a Vite PWA and Capacitor mobile app scaffold for Android and iOS.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
