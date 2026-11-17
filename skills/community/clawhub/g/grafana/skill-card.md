## Description:

Avoid common Grafana mistakes — query pitfalls, variable templating, alerting traps, and provisioning gotchas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, operators, and SREs use this skill for concise Grafana reminders covering dashboard variables, Prometheus query patterns, panel behavior, alerting, provisioning, data sources, and transformations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Grafana configuration guidance may be applied in an environment where a reminder does not match the deployment's data source, alerting, or provisioning model.

Mitigation: Review the generated guidance against the target Grafana version, data source settings, and operational requirements before changing dashboards or alerts.

Risk: Browser-mode data source advice and TLS skip-verify reminders touch settings that can expose endpoints or weaken certificate validation if used carelessly.

Mitigation: Prefer server-side data source access and valid TLS certificates for production systems; treat browser mode and TLS skip-verify as exceptional choices that need security review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/grafana)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static reference guidance; no code execution or credential access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
