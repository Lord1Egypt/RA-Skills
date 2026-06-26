## Description: <br>
Automates OpenClaw VPS setup, applies security hardening, configures multi-agent systems and messaging integrations, and generates deployment documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Harvnk](https://clawhub.ai/user/Harvnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up or harden OpenClaw on Ubuntu or Debian VPS hosts, configure multi-agent workspaces, connect messaging platforms, and generate deployment-specific reference documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports clean available scan signals, but also notes that the target artifact was not available for a full artifact-backed review. <br>
Mitigation: Review the skill files and install metadata before installing, especially any commands, credentials, network access, or persistent setup steps. <br>
Risk: The skill guides VPS setup, SSH and firewall hardening, bot-token integrations, cron jobs, backups, and health checks, where incorrect configuration could disrupt access or expose services. <br>
Mitigation: Apply changes only on the intended host, verify generated commands and configuration before execution, restrict API and bot tokens, and test SSH, firewall, backup, and monitoring behavior after setup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Harvnk/openclaw-setup-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce setup-specific documentation, security checklists, and deployment instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
