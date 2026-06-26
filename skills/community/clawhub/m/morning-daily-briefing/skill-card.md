## Description: <br>
Creates a morning briefing with priorities, calendar, and key updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and individual operators use this skill to produce a concise daily briefing from available calendar, email, task, CRM, news, and optional weather context. It helps identify the day's schedule, top priorities, follow-ups, and near-term heads-up items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily briefings may expose private calendar, email, CRM, task, or note details if the agent has broad data access or posts the result to a shared channel. <br>
Mitigation: Confirm connected data sources before installation, limit access to the sources needed for the briefing, and send briefings only to private destinations unless the contents are appropriate for a wider audience. <br>
Risk: Scheduled briefings can create recurring automatic summaries that run without a fresh user prompt. <br>
Mitigation: Enable heartbeat or cron delivery only when recurring briefings are intended, and review the schedule and destination before deployment. <br>


## Reference(s): <br>
- [Daily Briefing ClawHub Release](https://clawhub.ai/1kalin/morning-daily-briefing) <br>
- [Context Packs](https://afrexai-cto.github.io/context-packs/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Concise Markdown briefing or recap] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include calendar items, email highlights, priorities, follow-ups, news, and optional weather when those data sources are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
