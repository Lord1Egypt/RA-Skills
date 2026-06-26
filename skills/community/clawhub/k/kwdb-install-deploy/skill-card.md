## Description: <br>
Triggered when the user wants to install or deploy KaiwuDB (kwdb, kaiwudb). Helps users complete script-based deployment of KaiwuDB clusters, including configuration file modification, installation command execution, cluster initialization, and status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kwdb](https://clawhub.ai/user/kwdb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database administrators use this skill to plan and execute user-confirmed KaiwuDB deployments on Linux hosts. It guides single-node and cluster installation, deployment configuration, installation command execution, initialization, status checks, and failure reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide privileged KaiwuDB deployment changes on a target host. <br>
Mitigation: Use it only on intended hosts, require an explicit maintenance window and backup for production systems, and review sudo, systemctl, and deploy.sh commands before execution. <br>
Risk: Incorrect installation parameters can affect ports, data directories, security mode, or cluster connectivity. <br>
Mitigation: Confirm every generated deploy.cfg value and the installation package path before running deployment commands; do not rely on guessed defaults. <br>


## Reference(s): <br>
- [KWDB Install Deploy on ClawHub](https://clawhub.ai/kwdb/kwdb-install-deploy) <br>
- [KaiwuDB Script Deployment Guide](references/installation_guide.md) <br>
- [KaiwuDB Common Issues and Solutions](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before applying installation parameters or running privileged deployment commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
