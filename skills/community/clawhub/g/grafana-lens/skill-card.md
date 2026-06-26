## Description: <br>
Grafana Lens gives agents Grafana tools for querying metrics, logs, and traces; creating dashboards and alerts; running security and SRE investigations; pushing custom telemetry; and managing Grafana Alloy data collection pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awsome-o](https://clawhub.ai/user/awsome-o) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, SREs, and operators use this skill to let an agent inspect Grafana data, build dashboards, manage alerts, investigate incidents, and configure Alloy-based data collection pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over Grafana resources. <br>
Mitigation: Install only when agent-operated Grafana access is intended, use a dedicated least-privilege Grafana token, and require human approval for deletes, alert silences, notification routing, and Alloy pipeline changes. <br>
Risk: Conversation content is exported to telemetry by default. <br>
Mitigation: Set otlp.captureContent to false unless prompts and completions are explicitly meant to be stored in Grafana, Loki, or Tempo. <br>
Risk: Telemetry backends may contain sensitive operational or conversation data. <br>
Mitigation: Restrict access to Grafana, Loki, Tempo, Prometheus, and related telemetry backends to authorized users. <br>
Risk: Alloy pipeline changes can alter data collection behavior. <br>
Mitigation: Review generated pipeline changes before applying them and require human approval for pipeline creation, deletion, or credential-sensitive configuration. <br>


## Reference(s): <br>
- [Grafana Lens README](README.md) <br>
- [Agent Metrics Reference](references/agent-metrics.md) <br>
- [Alloy Component Reference](references/alloy-components.md) <br>
- [Alloy Pipeline Recipes](references/alloy-pipelines.md) <br>
- [Dashboard Composition Guide](references/dashboard-composition.md) <br>
- [External Data Naming Conventions and Integration Patterns](references/external-data.md) <br>
- [SRE Investigation Patterns](references/sre-investigation.md) <br>
- [Grafana Lens on ClawHub](https://clawhub.ai/awsome-o/grafana-lens) <br>
- [OpenClaw](https://openclaw.com) <br>
- [Grafana Alloy Documentation](https://grafana.com/docs/alloy/latest/) <br>
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with query snippets, dashboard or alert guidance, setup commands, and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Grafana dashboard links, PromQL, LogQL, TraceQL, Alloy configuration guidance, and human confirmation prompts for destructive actions.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
