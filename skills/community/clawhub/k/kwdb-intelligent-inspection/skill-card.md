## Description: <br>
Run KaiwuDB inspection and health-check tasks for database health checks, metrics collection, anomaly detection, and inspection report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kwdb](https://clawhub.ai/user/kwdb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Database administrators and support engineers use this skill to inspect KaiwuDB or KWDB clusters, collect metrics and slow statement telemetry, optionally apply user-requested anomaly rules, and produce a Markdown health-check report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches KaiwuDB admin telemetry over HTTP from user-specified hosts and ports. <br>
Mitigation: Run it only from a trusted admin environment, confirm the exact target hosts and ports before collection, and avoid untrusted networks. <br>
Risk: Slow statement telemetry can expose SQL text, application names, users, database names, and error messages. <br>
Mitigation: Review and redact raw slow-query output before sharing it outside approved operational or support channels. <br>
Risk: Inspection results may be misleading if run against the wrong cluster, unsupported TLS mode, or an incomplete scope. <br>
Mitigation: Follow the required confirmation workflow, stop when TLS mode is detected, and document partial or incomplete multi-node evidence in the report. <br>


## Reference(s): <br>
- [KWDB Intelligent Inspection on ClawHub](https://clawhub.ai/kwdb/kwdb-intelligent-inspection) <br>
- [Inspection Requirements Confirmation](references/inspection-requirements-confirmation.md) <br>
- [Port Listening Detection Reference](references/inspection-port-listening-reference.md) <br>
- [Time Series Metrics Script Usage](references/ts-metrics-script-usage.md) <br>
- [Slow Statements Script Usage](references/statements-script-usage.md) <br>
- [Report Template](references/report-template.md) <br>
- [Output Rules](references/output-rules.md) <br>
- [Anomaly Rules](references/anomaly-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown inspection report with metric tables, anomaly notes when requested, and optional raw JSON from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-confirmed hosts, ports, inspection scope, and unsupported TLS status before collection; slow-query output may contain SQL text, user names, database names, and errors.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
