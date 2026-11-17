## Description:

月嫂助手 generates an interactive HTML dashboard for maternity nurses, confinement centers, and maternal-care teams to manage newborn care, postpartum care, meal planning, health monitoring, medication tracking, daily logs, family reports, and handoff summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External maternity-care providers use this skill to create a local browser dashboard for tracking a 28-day postpartum service period, including infant and mother health metrics, meals, medications, care notes, family-facing reports, and final handoff records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive mother and infant health data may be stored locally without enough privacy disclosure.

Mitigation: Use only on trusted private devices, avoid regulated medical records, and add clear privacy notices before broader deployment.

Risk: Browser-side rendering and JSON import behavior may expose users to unsafe imported content.

Mitigation: Import backups only from trusted sources and add validation plus input/output escaping before production use.

Risk: Bash access is allowed even though the dashboard primarily uses a local HTML artifact.

Mitigation: Remove unnecessary Bash access or require review of any shell commands before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/nanny-assistant)
- [Chart.js 4.4.0 browser dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Interactive HTML dashboard with local JSON persistence and copyable text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses browser localStorage for care records and supports JSON backup import/export.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
