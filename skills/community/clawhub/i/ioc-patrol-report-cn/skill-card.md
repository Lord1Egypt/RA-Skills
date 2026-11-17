## Description:

Ioc Patrol Report generates daily or weekly IOC patrol reports for smart buildings and campuses by analyzing device status, alarms, energy use, and work orders, with Markdown or HTML report output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Facility operations teams, property managers, and developers use this skill to generate IOC patrol reports for smart buildings, campuses, commercial complexes, industrial parks, hospitals, schools, and data centers. The reports summarize operational status, alert handling, energy trends, work order progress, and maintenance recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence says this release ships a plaintext remote PostgreSQL admin-style credential and uses it by default.

Mitigation: Do not install or run this version until the publisher removes the packaged credential, rotates the exposed password, and replaces the account with a least-privilege reporting role.

Risk: Security evidence says environment or secret-manager credentials do not actually take precedence over the packaged database credential.

Mitigation: Require environment or secret-manager credentials to override packaged defaults before any database connection is attempted.

Risk: Security evidence says generated reports should clearly distinguish live data from mock data.

Mitigation: Label report data sources explicitly and require an intentional mock-data mode for non-production report generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/ioc-patrol-report-cn)
- [Report template](assets/report-template.md)
- [Generated daily report example](reports/daily-2026-03-20.md)
- [Generated weekly report example](reports/weekly-2026-W10.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates daily or weekly report files in the configured reports directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
