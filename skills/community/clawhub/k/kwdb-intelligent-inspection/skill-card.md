## Description:

Run KaiwuDB inspection and health-check tasks for database health checks, metrics collection, anomaly detection, and inspection report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwdb](https://clawhub.ai/user/kwdb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to inspect KaiwuDB clusters, collect time-series and slow-statement data, apply optional anomaly checks, and produce inspection reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inspection reports and raw JSON may expose SQL text, usernames, database names, and error details.

Mitigation: Run against hosts you administer and handle generated reports and raw outputs as sensitive operational data.

Risk: The skill probes network ports and collects data from KaiwuDB admin endpoints.

Mitigation: Use it only on authorized KaiwuDB clusters, preferably over trusted networks or tunnels, and confirm target hosts, ports, and scope before collection.

Risk: TLS-enabled KaiwuDB deployments are not supported by the artifact workflow.

Mitigation: Stop inspection when TLS mode is detected and use an approved TLS-capable process instead.

Risk: Single snapshots or incomplete multi-node evidence can lead to misleading anomaly judgments.

Mitigation: Document sampling windows, distinguish observed from inferred data, and require explicit thresholds for configurable anomaly checks.

## Reference(s):

- [Anomaly Rules](references/anomaly-rules.md)
- [Port Listening Detection Reference](references/inspection-port-listening-reference.md)
- [Inspection Requirements Confirmation](references/inspection-requirements-confirmation.md)
- [Metric Types](references/metric-types.md)
- [Output Rules](references/output-rules.md)
- [Report Template](references/report-template.md)
- [Slow Statements Script Usage](references/statements-script-usage.md)
- [Time Series Metrics Script Usage](references/ts-metrics-script-usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, json, guidance]

**Output Format:** [Markdown inspection report with optional JSON and tabular command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should identify data sources and assumptions; raw JSON and report content may include SQL text, usernames, database names, and error details.]

## Skill Version(s):

1.2.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
