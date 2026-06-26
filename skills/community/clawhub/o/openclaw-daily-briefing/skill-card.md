## Description: <br>
Generates a concise weekday morning briefing that combines weather, calendar, task, news, and commute context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangkai258](https://clawhub.ai/user/yangkai258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual users use this skill to prepare for the workday with a single morning summary of weather, meetings, due tasks, news, and practical suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefings may include personal or work-sensitive weather, calendar, task, news, and commute context. <br>
Mitigation: Review the permissions and data access of the dependent weather, calendar, task, and news skills before enabling scheduled or automated use. <br>
Risk: The included weather helper contacts wttr.in unless it is replaced or disabled. <br>
Mitigation: Replace the weather helper with an approved provider or disable external weather lookup when outbound requests are not appropriate. <br>
Risk: Enterprise WeChat calendar and task integrations may expose organizational schedule and todo data. <br>
Mitigation: Confirm Enterprise WeChat credentials, scopes, and recipients before enabling those integrations. <br>


## Reference(s): <br>
- [OpenClaw Daily Briefing on ClawHub](https://clawhub.ai/yangkai258/openclaw-daily-briefing) <br>
- [Publisher profile: yangkai258](https://clawhub.ai/user/yangkai258) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style briefing text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May incorporate weather, calendar, task, news, and commute context when dependent skills or APIs are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
