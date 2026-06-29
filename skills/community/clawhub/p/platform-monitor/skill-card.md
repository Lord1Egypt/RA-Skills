## Description: <br>
全平台状态监控助手，用于监控 AI 平台可达性、关键词变化、响应时间、竞品动态，并支持飞书、微信、钉钉通知、定时巡检和健康度评分。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laozhang-tou](https://clawhub.ai/user/laozhang-tou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external agent users use this skill to check AI platform availability, custom URLs, product pages, announcements, and competitor changes. It supports one-off checks, saved platform configurations, notification reports, and scheduled monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes periodic web requests to monitored platforms and custom URLs. <br>
Mitigation: Use it only for URLs you intend to monitor, and avoid adding sensitive internal URLs unless that monitoring is approved. <br>
Risk: The skill writes local monitoring configuration and history files. <br>
Mitigation: Review stored configuration for webhook URLs or private targets, and delete local config and history files when monitoring is no longer needed. <br>
Risk: The installation flow may add cron entries or Windows scheduled tasks for recurring checks. <br>
Mitigation: Review scheduled tasks before enabling them, and remove the task if you stop using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laozhang-tou/platform-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, configuration snippets, and JSON monitoring results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Monitoring results include platform status, response time, alerts, summaries, and optional notification-ready reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
