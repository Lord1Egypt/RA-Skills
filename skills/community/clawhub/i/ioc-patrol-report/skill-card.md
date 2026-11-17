## Description:

为 IOC（智能运营中心）生成智能巡检报告，分析设备状态、报警记录、能耗数据和工单进度，并生成巡检日报或周报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams, property managers, and facility engineers use this skill to generate IOC patrol reports for smart buildings, commercial complexes, industrial parks, and similar environments. It summarizes device availability, alarms, work orders, energy use, and operational recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged configuration includes a real-looking remote PostgreSQL credential and the report generator attempts to use configured database settings automatically.

Mitigation: Remove the packaged credential before installation, rotate any exposed credential, and replace config.yaml with environment-specific settings.

Risk: Generated reports may contain sensitive facility, operations, or personnel-access information.

Mitigation: Use a dedicated read-only reporting database account, restrict access to required tables, and review generated reports before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/ioc-patrol-report)
- [README](README.md)
- [Report template](assets/report-template.md)
- [Configuration example](config.yaml)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces daily or weekly IOC patrol report files; generated reports may include facility operations data.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json; pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
