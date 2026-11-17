## Description: <br>
网络监控免费版 helps personal developers and small teams monitor website, API, and host availability with ICMP ping checks, HTTP health checks, email alerts, availability statistics, and basic visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, independent project maintainers, and small teams use this skill to set up lightweight local availability monitoring for blogs, APIs, hosts, and home network targets. It can guide agents to create monitoring configuration, run ping or HTTP checks, produce availability summaries, and configure email alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to run network checks from the user's machine. <br>
Mitigation: Install and use it only for targets you intend to monitor, and review proposed commands before execution. <br>
Risk: The skill includes recurring cron or systemd monitoring examples. <br>
Mitigation: Review scheduled-task changes before applying them and document how to disable or remove the recurring job. <br>
Risk: Email alert setup may involve SMTP app passwords or other credentials. <br>
Mitigation: Keep SMTP credentials out of shared files, use app-specific passwords where available, and restrict file permissions for local configuration. <br>
Risk: Monitoring logs and configuration may be stored under ~/.ping-monitor. <br>
Mitigation: Confirm the storage location, retention expectations, and cleanup path before enabling persistent monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ping-monitor-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, shell, JSON, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local files under ~/.ping-monitor, recurring cron/systemd monitoring, network checks from the user's machine, and email alert configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
