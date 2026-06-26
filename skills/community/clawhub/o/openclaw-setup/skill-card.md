## Description: <br>
Set up a complete OpenClaw personal AI assistant from scratch using Claude Code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j540](https://clawhub.ai/user/j540) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to deploy and configure a personal OpenClaw assistant on AWS with Telegram, API keys, optional Google Workspace access, security hardening, persistence, and user-specific memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to administer a cloud server and configure persistent automation with live credentials. <br>
Mitigation: Use fresh least-privilege credentials, review privileged commands before execution, and know how to stop the service and revoke tokens. <br>
Risk: Optional Google Workspace and messaging integrations can expose sensitive personal data to a persistent assistant. <br>
Mitigation: Limit OAuth scopes to the requested integrations, avoid unnecessary data access, and delete stored memory when retiring the deployment. <br>
Risk: The setup installs software from external package and repository sources. <br>
Mitigation: Verify package sources and repository URLs before running install commands. <br>


## Reference(s): <br>
- [OpenClaw Setup Guide: Your Personal AI Assistant](references/openclaw-installation-human-guide.md) <br>
- [OpenClaw Setup on ClawHub](https://clawhub.ai/j540/openclaw-setup) <br>
- [gogcli GitHub repository](https://github.com/steipete/gogcli.git) <br>
- [NodeSource Node.js 22 setup script](https://deb.nodesource.com/setup_22.x) <br>
- [OpenClaw community Discord](https://discord.com/invite/clawd) <br>
- [OpenClaw documentation](https://docs.clawd.bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline bash and JSON configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces step-by-step setup guidance for an agent to execute with user-provided credentials and cloud access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
