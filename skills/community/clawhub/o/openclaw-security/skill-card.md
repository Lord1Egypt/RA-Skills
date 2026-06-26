## Description: <br>
Unified security suite for agent workspaces that installs, configures, and orchestrates 11 OpenClaw security tools for integrity, secrets, permissions, network, audit, signing, supply chain, credentials, injection defense, compliance, and incident response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and workspace operators use this skill to install and coordinate OpenClaw security tools, run workspace health checks and scans, and initialize security baselines, signing, audit, and policy components. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can bulk-install, update, execute, and orchestrate companion tools across a workspace. <br>
Mitigation: Install only when the publisher and companion tools are trusted, review the tools before use, and run commands against an explicit workspace path. <br>
Risk: The update command may move important workspaces to latest companion-tool versions. <br>
Mitigation: Avoid unpinned latest-version updates in important workspaces unless the update has been reviewed and approved. <br>
Risk: The protect command can trigger automated changes such as quarantine, blocking, revocation, rotation, containment, or remediation. <br>
Mitigation: Back up the workspace first and run protect only when automated remediation is intended. <br>


## Reference(s): <br>
- [Openclaw Security on ClawHub](https://clawhub.ai/AtlasPA/openclaw-security) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [OpenClaw Warden](https://github.com/AtlasPA/openclaw-warden) <br>
- [OpenClaw Sentry](https://github.com/AtlasPA/openclaw-sentry) <br>
- [OpenClaw Sentinel](https://github.com/AtlasPA/openclaw-sentinel) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate companion security tools against an explicit workspace path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
