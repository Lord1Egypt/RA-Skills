## Description: <br>
Generate interactive analytics dashboards from CRM data using DuckDB queries and Recharts-compatible report JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aspenas](https://clawhub.ai/user/aspenas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, operators, and developers use this skill to turn natural-language CRM pipeline questions into DuckDB SQL queries, analytics summaries, and interactive dashboard report JSON for Ironclaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query sensitive CRM, sales, or customer data. <br>
Mitigation: Review the skill before installation, use it only with explicit pipeline datasets, and prefer read-only SELECT-style queries. <br>
Risk: The skill can save reports into the workspace. <br>
Mitigation: Confirm output paths and report contents before saving generated .report.json files. <br>
Risk: The skill describes recurring cron-based report generation. <br>
Mitigation: Create scheduled jobs only when the schedule, payload, and disable process are understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aspenas/ironclaw-pipeline-analytics) <br>
- [Publisher Profile](https://clawhub.ai/user/aspenas) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with SQL and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Recharts-compatible report JSON, DuckDB SQL query patterns, saved .report.json report definitions, and cron schedule configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
