## Description: <br>
Glances is a cross-platform system monitoring skill that helps agents install, run, interpret, and configure Glances for terminal, Web, API, export, and remote monitoring workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and system administrators use this skill to monitor local or remote machines with Glances, inspect resource bottlenecks, configure Web/API modes, and export metrics for analysis or observability workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network-exposed Glances Web/API or server modes can reveal host monitoring data to untrusted networks. <br>
Mitigation: Prefer localhost binding or SSH tunnels, require authentication where supported, and review any firewall or bind-address changes before execution. <br>
Risk: Docker socket mounts, host networking, docker group changes, and persistent services can broaden host access. <br>
Mitigation: Avoid docker.sock mounts, host networking, docker group membership changes, systemd units, or cron jobs unless they are necessary and manually approved. <br>
Risk: Commands that forcefully terminate processes or handle tokens and SMTP passwords can disrupt workloads or expose secrets. <br>
Mitigation: Manually approve process-kill commands and keep tokens, passwords, and export credentials out of shared logs or generated files. <br>


## Reference(s): <br>
- [ClawHub Glances listing](https://clawhub.ai/cn-big-cabbage/glances) <br>
- [Glances homepage](https://nicolargo.github.io/glances/) <br>
- [Glances documentation](https://glances.readthedocs.io/) <br>
- [Glances GitHub repository](https://github.com/nicolargo/glances) <br>
- [Glances Docker Hub image](https://hub.docker.com/r/nicolargo/glances) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and monitoring interpretations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that install packages, start local services, expose monitoring ports, query APIs, or write Glances configuration files.] <br>

## Skill Version(s): <br>
0.1.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
