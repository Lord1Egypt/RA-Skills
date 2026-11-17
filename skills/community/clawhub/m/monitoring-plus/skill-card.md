## Description:

Enhanced monitoring with Prometheus, Grafana, Loki, alerting rules, dashboard templates, and SLO/SLI tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to draft monitoring, logging, alerting, dashboard, and SLO/SLI guidance for services using Prometheus, Grafana, Loki, and Alertmanager.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Starter alerting and Loki configurations may be unsafe for production if copied without review.

Mitigation: Replace placeholder credentials, enable authentication and network controls for monitoring endpoints, and review configurations before deployment.

Risk: Alert messages may expose internal service names or incident details when sent to third-party receivers.

Mitigation: Review alert labels, annotations, and receiver routing before sending notifications outside trusted systems.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with YAML, JSON, PromQL, and LogQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces documentation and starter configuration examples; no executable tool output is generated.]

## Skill Version(s):

2.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
