## Description:

Grafana inspection skill for API-based dashboard checks, batch dashboard discovery, alert and datasource review, and JSON or Markdown report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diluke1600](https://clawhub.ai/user/diluke1600)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SRE teams use this skill to inspect Grafana dashboards, alerts, and data sources, then produce operational health reports. It is suited for configured Grafana environments where reports and credentials can be stored securely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Grafana API tokens or username/password credentials may be exposed or granted broader access than needed.

Mitigation: Use a read-only, narrowly scoped Grafana API token, avoid username/password credentials when possible, and protect configuration and generated report files.

Risk: A bundled inspection script disables TLS certificate verification while sending Grafana credentials.

Mitigation: Fix or avoid scripts/inspection_report.py until TLS verification is enabled and trusted certificates are configured.

Risk: Documentation overstates browser screenshot and Feishu reporting capabilities relative to the security summary.

Mitigation: Treat the release as producing API-based JSON and Markdown reports unless additional behavior is independently validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diluke1600/skills/grafana-inspector)
- [Publisher profile](https://clawhub.ai/user/diluke1600)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, markdown]

**Output Format:** [Text guidance plus generated JSON and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Grafana URL and preferably a read-only Grafana API token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
