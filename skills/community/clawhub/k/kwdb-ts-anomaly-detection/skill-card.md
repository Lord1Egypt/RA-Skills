## Description:

Automates end-to-end anomaly detection for time-series data stored in KaiwuDB / KWDB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwdb](https://clawhub.ai/user/kwdb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to inspect KWDB/KaiwuDB time-series tables for spikes, dips, drift, and other outliers in numeric telemetry columns. It guides connection validation, SQL refinement, 3-sigma STL detection, optional column-rule filtering, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles KWDB account credentials and database output files.

Mitigation: Use a dedicated read-only database user, avoid sensitive production data, and treat local /tmp reports and intermediate files as sensitive.

Risk: The security evidence says the local scripts run broad SQL and need review.

Mitigation: Review SQL before execution, enforce read-only access, add time filters or limits, and prefer a revised version with read-only SQL enforcement and parameterized queries.

Risk: The security guidance flags command-line passwords, TLS, timeouts, and generated HTML escaping as areas needing improvement.

Mitigation: Prefer a revised version that removes command-line passwords, uses authenticated TLS with timeouts, and safely escapes generated HTML.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kwdb/skills/kwdb-ts-anomaly-detection)
- [Publisher Profile](https://clawhub.ai/user/kwdb)
- [Workflow](references/workflow.md)
- [Constraints](references/constraints.md)
- [Metadata Query](references/metadata-query.md)
- [SELECT Query Reference](references/ts-select.md)
- [Column Comment Rules](references/column-comment.md)
- [Error Handling](references/error-handling.md)
- [Markdown Report Template](references/report-template.md)
- [HTML Report Template](references/report-template-html.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [User-facing instructions and SQL/shell commands, plus optional Markdown or HTML anomaly reports and JSON intermediate files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Detection focuses on timestamped numeric KWDB/KaiwuDB columns, uses STL plus 3-sigma residual thresholds, and writes temporary query and detection files under /tmp before cleanup.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
