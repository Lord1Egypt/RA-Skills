## Description:

Guides agents through production observability for Go services, including structured logging, Prometheus metrics, OpenTelemetry tracing, profiling, RUM, alerting, and Grafana dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to instrument, review, and audit Go services for production observability across logs, metrics, traces, profiles, RUM events, alerts, and dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated observability code may introduce unsafe telemetry or privacy-sensitive endpoints.

Mitigation: Review generated code before merging and confirm telemetry behavior against project privacy and security requirements.

Risk: Analytics and user data workflows may collect or expose personal data without adequate controls.

Mitigation: Require authenticated, authorized, and audited export or deletion workflows, and enforce consent and data minimization for analytics.

Risk: Metrics, traces, and logs may include raw URLs or user-controlled identifiers.

Mitigation: Use bounded route patterns and sanitized fields rather than raw paths, user identifiers, or sensitive values.

Risk: Profiling endpoints can expose sensitive runtime data.

Mitigation: Protect profiling with HTTPS, authentication, authorization, and sanitized logging.

Risk: Parallel sub-agent audits may inspect private repository contents more broadly than intended.

Mitigation: Approve any multi-agent audit scope before running it on private repositories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samber/skills/golang-observability)
- [Project Homepage](https://github.com/samber/cc-skills-golang)
- [Structured Logging](references/logging.md)
- [Metrics Collection](references/metrics.md)
- [Distributed Tracing](references/tracing.md)
- [Profiling](references/profiling.md)
- [Real User Monitoring](references/rum.md)
- [Alerting](references/alerting.md)
- [Grafana Dashboards](references/dashboards.md)
- [Awesome Prometheus Alerts](https://samber.github.io/awesome-prometheus-alerts/)
- [Prometheus Naming Practices](https://prometheus.io/docs/practices/naming/)
- [Go Host and Runtime Metrics Dashboard](https://grafana.com/grafana/dashboards/21221-go-host-runtime-metrics-dashboard/)
- [Go Processes Dashboard](https://grafana.com/grafana/dashboards/6671-go-processes/)
- [Go Metrics Dashboard](https://grafana.com/grafana/dashboards/10826-go-metrics/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Go, YAML, PromQL, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Go tooling for project-specific implementation.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
