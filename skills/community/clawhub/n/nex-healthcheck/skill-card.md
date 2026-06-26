## Description: <br>
Nex Healthcheck helps agents monitor websites, APIs, SSL certificates, DNS, Docker containers, systemd services, SSH checks, disk usage, incidents, uptime, and optional Telegram alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, system administrators, agency operators, and IT teams use this skill to configure and run health checks for production services, inspect uptime and incident history, and produce concise status summaries for users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured service names, paths, container names, and SSH command targets can flow into local or remote shell commands. <br>
Mitigation: Run the skill under a low-privilege local account, use low-privilege SSH keys, and only add check definitions from trusted operators. <br>
Risk: The config command can reveal Telegram credential material. <br>
Mitigation: Do not use real Telegram secrets with the config command until token masking is fixed; prefer controlled environment variables and rotate any exposed tokens. <br>
Risk: Telegram notifications send infrastructure status data to an external service. <br>
Mitigation: Enable Telegram only for approved environments and avoid including sensitive host, service, or incident details in notification targets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nexaiguy/nex-healthcheck) <br>
- [Nex AI homepage](https://nex-ai.be) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text CLI output summarized in Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include health status, response times, SSL expiry windows, DNS results, container or service state, uptime percentages, incident history, and optional Telegram notification content.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
