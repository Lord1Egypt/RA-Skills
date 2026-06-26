## Description: <br>
Ioc Patrol Report generates daily and weekly IOC patrol reports for smart building and campus operations by analyzing device status, alarm records, energy use, and work order progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External facilities, property-management, and smart-building operations teams use this skill to produce routine IOC patrol reports from operational database data, covering equipment availability, alarms, energy consumption, work orders, and maintenance recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes a real remote PostgreSQL credential in its bundled database configuration. <br>
Mitigation: Remove or replace the bundled database configuration before installation, rotate any exposed credential, and use environment-managed secrets for database access. <br>
Risk: The report generator queries hard-coded operational tables that may include sensitive building operations data. <br>
Mitigation: Verify the exact tables and fields queried before running the skill, restrict database permissions to the minimum required scope, and test against non-production data first. <br>
Risk: Generated reports may contain operational status, alarm, energy, or work-order details. <br>
Mitigation: Store report outputs only in access-controlled locations and review generated content before sharing outside the operations team. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/ioc-patrol-report-cn) <br>
- [Publisher profile](https://clawhub.ai/user/onlyloveher) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with command-line and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates daily or weekly report files and may also produce HTML output when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
