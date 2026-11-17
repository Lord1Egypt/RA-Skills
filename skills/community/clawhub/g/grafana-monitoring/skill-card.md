## Description:

Grafana HTTP API integration. Inspect dashboards, folders, data sources, alert rules, and teams. Use this skill when users want to query observability data, inspect monitoring resources, or manage Grafana dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect Grafana observability resources and manage dashboards, folders, data sources, alert rules, and teams through authenticated Grafana API tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected Grafana credentials can expose or change resources within the API key or service account permissions.

Mitigation: Use a least-privilege Grafana API key or service account and review the connected credential scope before installation.

Risk: Create, update, or delete operations can modify dashboards, folders, data sources, alert rules, teams, or permissions.

Mitigation: Preview write actions and require explicit user confirmation of the target resource and intended effect before execution.

## Reference(s):

- [Grafana HTTP API Documentation](https://grafana.com/docs/grafana/latest/developers/http_api/)
- [Grafana Dashboard API](https://grafana.com/docs/grafana/latest/developers/http_api/dashboard/)
- [Grafana Alerting API](https://grafana.com/docs/grafana/latest/developers/http_api/alerting/)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/grafana-monitoring)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Grafana API tool-call guidance, connection checks, write previews, and troubleshooting steps.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
