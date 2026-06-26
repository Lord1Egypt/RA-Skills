## Description: <br>
This skill helps an agent manage OKR and KPI work records by creating workspace JSON data for daily logs, weekly plans, recurring reports, and OKR progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zerosloney](https://clawhub.ai/user/zerosloney) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and knowledge workers use this skill to record daily work, plan weekly tasks, generate weekly, monthly, quarterly, and yearly reports, and track work against OKR goals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores OKR, work-history, and report data as local JSON files in the workspace. <br>
Mitigation: Use it only in workspaces where that data may be stored, and avoid entering secrets or sensitive customer data. <br>
Risk: The skill can update past logs and plans, which may affect report accuracy. <br>
Mitigation: Review edits to historical JSON records before relying on generated weekly, monthly, quarterly, or yearly reports. <br>
Risk: Optional Gateway Cron jobs can generate reports on a recurring schedule. <br>
Mitigation: Enable scheduled weekly or monthly jobs only when recurring report generation is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zerosloney/okr-work-manager) <br>
- [Data schema reference](references/data-schema.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [Basic usage examples](examples/basic-usage.md) <br>
- [Advanced usage examples](examples/advanced-usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown responses plus workspace JSON records, plans, reports, and OKR configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates data under .okr-work-manager/ in the active workspace when the agent follows the skill.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
