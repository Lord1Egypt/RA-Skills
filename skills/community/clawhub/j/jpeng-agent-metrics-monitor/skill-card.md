## Description:

Provides monitoring and alerting for agent abnormal behavior metrics with Prometheus and Grafana support, including P99 latency, error rates, anomaly detection, and custom alert rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to instrument agents with latency, error-rate, success-rate, alerting, and anomaly-detection metrics. It can export Prometheus-compatible metrics and generate Grafana dashboard configuration for monitoring agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted metric names or label values can create malformed or misleading monitoring output.

Mitigation: Use trusted or pre-normalized metric names and labels before exporting Prometheus metrics.

Risk: High-cardinality labels can make monitoring systems noisy or expensive to operate.

Mitigation: Avoid labels such as request IDs, raw URLs, and other unbounded values.

Risk: Rate helpers report lifetime ratios rather than true rolling-window rates.

Mitigation: Document this behavior for users and rely on Prometheus or another time-series system for rolling-window rate calculations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-agent-metrics-monitor)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, code, configuration]

**Output Format:** [JavaScript API results, Prometheus exposition text, and Grafana dashboard JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [In-memory metrics collection with configurable retention and alert history limits.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
