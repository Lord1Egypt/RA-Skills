## Description:

Set up observability for applications and infrastructure with metrics, logs, traces, and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to choose and configure monitoring approaches for applications and infrastructure, including uptime checks, application performance monitoring, centralized logs, Prometheus/Grafana metrics, and alerting practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring examples can expose service status, host telemetry, logs, traces, or operational details if deployed on public interfaces.

Mitigation: Bind monitoring ports to localhost or private networks, require authentication and TLS, apply firewall rules, and redact logs and traces before collection or export.

Risk: Some examples install or run third-party packages, container images, and setup tools that may change over time.

Mitigation: Review examples before use, pin package and image versions, and harden configurations before installing services in production.

Risk: Alert messages and monitoring notifications can leak secrets or sensitive operational details.

Mitigation: Keep alert payloads free of secrets, route notifications only to approved channels, and limit retained log and trace data to what is operationally necessary.

## Reference(s):

- [Monitoring skill page](https://clawhub.ai/ivangdavila/skills/monitoring)
- [Monitoring overview](artifact/SKILL.md)
- [Simple Monitoring](artifact/simple.md)
- [Application Performance Monitoring](artifact/apm.md)
- [Prometheus + Grafana Stack](artifact/prometheus.md)
- [Centralized Logging](artifact/logs.md)
- [Alerting Best Practices](artifact/alerting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for selecting, configuring, and operating monitoring tools.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
