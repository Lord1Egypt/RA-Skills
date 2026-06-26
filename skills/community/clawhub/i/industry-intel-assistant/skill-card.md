## Description: <br>
行业情报收集与分析助手，自动监控特定行业动态、抓取热点资讯、生成结构化情报简报，并支持多渠道推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business, research, and operations teams use this skill to monitor industry or competitor topics, gather current news with Tavily, and produce scheduled intelligence briefs for internal distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduling flow may allow shell command injection when creating recurring intelligence jobs. <br>
Mitigation: Review and patch the scheduling script before use, and treat query, schedule, timezone, and channel values as untrusted input. <br>
Risk: Recurring jobs can persistently send report contents to configured channels. <br>
Mitigation: Confirm every destination channel before enabling delivery, avoid sensitive queries, and document how to list, disable, and remove the recurring job. <br>
Risk: The skill reads a Tavily API key and uses it for external search requests. <br>
Mitigation: Store the key in a secret store or environment variable, rotate it when needed, and avoid sending confidential topics or source material to the search service. <br>


## Reference(s): <br>
- [行业情报助手 — 快速上手指南](artifact/references/intro.md) <br>
- [Tavily](https://tavily.com) <br>
- [ClawHub skill page](https://clawhub.ai/xuyongliang-eccom/industry-intel-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/xuyongliang-eccom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown intelligence briefs, JSON search results, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write report files locally, read a Tavily API key from configuration or environment variables, create recurring jobs, and send report contents to configured channels.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
