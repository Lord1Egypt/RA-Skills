## Description:

Grafana Lens gives agents Grafana tools for querying metrics, logs, and traces, creating dashboards and alerts, running SRE and security investigations, pushing custom telemetry, and managing Grafana Alloy data collection pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awsome-o](https://clawhub.ai/user/awsome-o)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and SRE teams use this skill to inspect Grafana data, build dashboards, configure alerts, investigate incidents, and set up telemetry collection pipelines from natural language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Grafana service-account authority and can create or modify dashboards, alerts, annotations, and related Grafana resources.

Mitigation: Use a least-privilege Grafana token, scope access to the intended organization and datasources, and require review before destructive operations.

Risk: The skill can send agent telemetry, including sensitive conversation content by default, to the configured OTLP backend.

Mitigation: In shared, cloud, or sensitive environments, set otlp.captureContent=false and consider disabling otlp.forwardAppLogs, otlp.logs, or otlp.traces until content handling is reviewed.

Risk: Optional Alloy pipeline management can write and reload collection configuration, including raw pipeline configs and delete actions.

Mitigation: Enable Alloy only with a tightly controlled config directory, prefer validated recipes, review raw configs before use, and confirm delete actions with the user.

Risk: The server security verdict is suspicious because the skill combines broad Grafana mutation authority with telemetry export behavior.

Mitigation: Install only after reviewing the requested permissions, telemetry settings, and the security guidance from the release evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awsome-o/skills/grafana-lens)
- [Dashboard Composition Guide](references/dashboard-composition.md)
- [Alloy Pipeline Recipes](references/alloy-pipelines.md)
- [Alloy Component Reference](references/alloy-components.md)
- [SRE Investigation Patterns](references/sre-investigation.md)
- [External Data Integration Patterns](references/external-data.md)
- [Agent Metrics Reference](references/agent-metrics.md)
- [OpenClaw](https://openclaw.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text with Grafana query results, dashboard and alert guidance, PromQL/LogQL/TraceQL snippets, shell commands, and configuration details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include links to Grafana dashboards or rendered panels when configured.]

## Skill Version(s):

0.5.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
