## Description:

Monitoring infrastructure assessment covering Grafana dashboard analysis, PromQL query validation, alert rule evaluation, SLA/SLO reporting review, and Prometheus data source health checks for network operations environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and network operations teams use this skill to audit Grafana dashboards, Prometheus data sources, PromQL queries, alert rules, and SLA/SLO reporting for monitoring coverage and reliability gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring audit outputs can expose sensitive operational details such as datasource URLs, alert routing, contact points, silences, and Prometheus configuration.

Mitigation: Use least-privilege Grafana Viewer access, keep tokens out of shared outputs, and review reports before distributing them outside the authorized operations team.

Risk: Dashboard, alert, or query recommendations may be incorrect if inventory, SLA/SLO targets, or baseline documentation are incomplete.

Mitigation: Validate findings against current network scope, service documentation, and operations runbooks before changing monitoring configuration.

## Reference(s):

- [CLI Reference - Grafana and Prometheus APIs](references/cli-reference.md)
- [Query Reference - PromQL Patterns for Network Monitoring](references/query-reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown report with command and PromQL snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only audit guidance; the skill does not create, modify, or delete dashboards, alerts, or data sources.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
