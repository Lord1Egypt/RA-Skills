## Description: <br>
Golang everyday observability for production services, covering structured logging with slog, Prometheus metrics, OpenTelemetry tracing, pprof/Pyroscope profiling, server-side RUM tracking, alerting, and Grafana dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add, review, or audit observability in Go services, including logs, metrics, traces, profiles, RUM events, alerts, and dashboards. It is intended for production monitoring work rather than one-off performance deep dives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telemetry examples may send sensitive data outside the service boundary through logs, traces, profiles, or analytics events. <br>
Mitigation: Review data fields before copying examples into production; avoid PII and secrets in telemetry and document what leaves the service. <br>
Risk: Metrics with unbounded labels such as user IDs or full URLs can create high-cardinality time series and degrade Prometheus performance. <br>
Mitigation: Use bounded labels such as route templates, methods, and status classes, and review proposed metric labels before deployment. <br>
Risk: RUM and analytics event tracking can create privacy and compliance obligations. <br>
Mitigation: Require consent checks, use stable non-PII user IDs, and provide data export or deletion paths where applicable. <br>
Risk: pprof endpoints and profiling backends can expose runtime details or increase operational cost. <br>
Mitigation: Protect profiling endpoints with authentication and authorization, toggle profiling through configuration, and enable continuous profiling only where the overhead is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-observability) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>
- [Project homepage](https://github.com/samber/cc-skills-golang) <br>
- [Structured Logging](references/logging.md) <br>
- [Metrics Collection](references/metrics.md) <br>
- [Distributed Tracing](references/tracing.md) <br>
- [Profiling](references/profiling.md) <br>
- [Real User Monitoring](references/rum.md) <br>
- [Alerting](references/alerting.md) <br>
- [Grafana Dashboards](references/dashboards.md) <br>
- [Awesome Prometheus Alerts](https://samber.github.io/awesome-prometheus-alerts/) <br>
- [Prometheus metric naming](https://prometheus.io/docs/practices/naming/) <br>
- [Go Host & Runtime Metrics dashboard](https://grafana.com/grafana/dashboards/21221-go-host-runtime-metrics-dashboard/) <br>
- [Go Processes dashboard](https://grafana.com/grafana/dashboards/6671-go-processes/) <br>
- [Go Metrics dashboard](https://grafana.com/grafana/dashboards/10826-go-metrics/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Go, YAML, PromQL, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose instrumentation changes, observability configuration, review findings, and audit guidance for Go services.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
