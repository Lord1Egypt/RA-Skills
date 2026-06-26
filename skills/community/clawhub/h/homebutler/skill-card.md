## Description: <br>
Homelab server operations via homebutler CLI/MCP, including system status, reports, inventory/topology, Docker management, app installation, backup drills, Wake-on-LAN, port scanning, alerts, backup/restore, and multi-server SSH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[higangssh](https://clawhub.ai/user/higangssh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, homelab operators, and agent users use Homebutler to inspect and administer local or configured servers through the homebutler CLI or MCP server. It helps summarize health, inspect inventory, manage Docker workloads, deploy self-hosted apps, and verify backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to run powerful server and data-changing operations, including purge, restore, deploy, upgrade, Docker stop/restart, and all-server commands. <br>
Mitigation: Confirm the exact server, app, and scope before acting, and require separate explicit approval before destructive, remote, upgrade, restore, or --all operations. <br>
Risk: Homelab commands may expose hostnames, IP addresses, service names, logs, or topology details. <br>
Mitigation: Summarize sensitive infrastructure details for shared contexts and avoid exposing raw JSON, logs, or network scan results unless the user explicitly approves. <br>
Risk: The skill depends on an external homebutler CLI that can administer local and configured remote systems. <br>
Mitigation: Install and use the CLI only in trusted environments, prefer key-based SSH authentication, and keep configuration files restricted to the owner. <br>


## Reference(s): <br>
- [Homebutler on ClawHub](https://clawhub.ai/higangssh/homebutler) <br>
- [homebutler CLI repository](https://github.com/Higangssh/homebutler) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, summaries, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands produce human-readable text by default and can use JSON output for automation when supported.] <br>

## Skill Version(s): <br>
2.3.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
