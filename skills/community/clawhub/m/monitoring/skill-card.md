## Description: <br>
Set up observability for applications and infrastructure with metrics, logs, traces, and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to choose and configure monitoring for applications and infrastructure, including uptime checks, metrics, logs, traces, dashboards, and alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copying the examples directly into production can leave monitoring services, dashboards, or alerting endpoints insufficiently hardened. <br>
Mitigation: Review and harden configurations before production use, restrict monitoring ports to trusted networks, and pin package or container versions when needed. <br>
Risk: Telemetry can expose secrets, personal data, headers, request bodies, stack traces, or sensitive logs to monitoring systems or vendors. <br>
Mitigation: Redact or minimize sensitive data before collection, protect Grafana and alerting secrets, and limit telemetry access to authorized users. <br>
Risk: Misconfigured alerting can create noise or missed incidents. <br>
Mitigation: Alert on actionable user impact, add runbooks for critical alerts, and test routing and escalation paths before relying on them. <br>


## Reference(s): <br>
- [ClawHub Monitoring Release](https://clawhub.ai/ivangdavila/monitoring) <br>
- [Monitoring Skill Overview](artifact/SKILL.md) <br>
- [Simple Monitoring](artifact/simple.md) <br>
- [Application Performance Monitoring](artifact/apm.md) <br>
- [Prometheus + Grafana Stack](artifact/prometheus.md) <br>
- [Centralized Logging](artifact/logs.md) <br>
- [Alerting Best Practices](artifact/alerting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell, YAML, JavaScript, TypeScript, JSON, and PromQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes monitoring tool comparisons, setup checklists, and example alerting, logging, tracing, and dashboard configurations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
