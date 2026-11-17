## Description:

Connects an agent to Grafana to inspect and manage dashboards, folders, data sources, annotations, teams, and alert rules through a user-authorized connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect Grafana monitoring resources and, with explicit approval, create or change dashboards, folders, data sources, annotations, and teams. It also documents optional event-driven and scheduled automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Grafana writes can change monitoring resources or team access.

Mitigation: Default to reads; confirm the exact resource and effect with the user before each write.

Risk: A connected account may grant broader Grafana access than the task needs.

Mitigation: Use least-privilege credentials and authorize only the required connection.

Risk: Optional functions, triggers, destinations, and watchers can run persistently or forward event data.

Mitigation: Approve each automation and destination separately; scope it narrowly and remove it when no longer needed.

## Reference(s):

- [Grafana skill on ClawHub](https://clawhub.ai/byungkyu/skills/grafana-api)
- [Publisher profile](https://clawhub.ai/user/byungkyu)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Grafana HTTP API documentation](https://grafana.com/docs/grafana/latest/developers/http_api/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown guidance, command and code examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-authorized connection; resource changes require explicit confirmation.]

## Skill Version(s):

1.2.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
