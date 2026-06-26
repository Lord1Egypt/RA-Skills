## Description: <br>
Analyzes Jiawei BlueKing ITSM ticket data with multi-process field mapping, handling recommendations, trend reports, frequent-issue detection, and SLA risk monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MichaelJochen](https://clawhub.ai/user/MichaelJochen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
IT service teams and operations analysts use this skill to analyze exported Jiawei BlueKing ITSM ticket data, generate daily, weekly, or monthly reports, recommend handling paths for new tickets, identify repeated issues, and monitor SLA timeout risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticket exports and generated reports can contain sensitive requester, assignee, incident, or operational data, especially when pushed to Enterprise WeChat. <br>
Mitigation: Review and redact reports before sharing, and avoid broad Enterprise WeChat groups for sensitive tickets. <br>
Risk: Optional ITSM API use can expose credentials or grant more access than the analysis task requires. <br>
Mitigation: Use least-privilege read-only API credentials if API access is added, and inspect referenced scripts before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MichaelJochen/openclaw-itsm-skill) <br>
- [Publisher profile](https://clawhub.ai/user/MichaelJochen) <br>
- [blueking-api.md](references/blueking-api.md) <br>
- [ticket-classification.md](references/ticket-classification.md) <br>
- [sla-policy.md](references/sla-policy.md) <br>
- [webhook-config.md](references/webhook-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and concise text guidance, with optional shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference CSV, Excel, or JSON ticket exports and optional Enterprise WeChat webhook delivery.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
