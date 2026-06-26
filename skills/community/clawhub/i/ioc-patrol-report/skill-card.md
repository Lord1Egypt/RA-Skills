## Description: <br>
为 IOC（智能运营中心）生成智能巡检报告，分析设备状态、报警记录、能耗数据和工单进度，并输出巡检日报或周报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Facilities, property operations, industrial park, and data center teams use this skill to generate IOC patrol reports from PostgreSQL-backed operational data or fallback mock data. It summarizes device availability, alarms, energy use, work orders, SLA status, and suggested follow-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes a real-looking remote PostgreSQL credential in config.yaml. <br>
Mitigation: Remove the bundled credential before use, rotate it if it is real, and configure a user-controlled secret for a least-privilege read-only database account. <br>
Risk: The report generator queries operational tables beyond the documentation summary, including personnel access data. <br>
Mitigation: Inspect and approve the SQL queries before connecting the skill to production data, and limit database permissions to the specific report fields required. <br>
Risk: Generated reports may use mock or incomplete data when database access fails. <br>
Mitigation: Verify the configured data source and treat each report as operationally unverified unless the data source and query results are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/ioc-patrol-report) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Report template](assets/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily or weekly report files under the configured reports directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
