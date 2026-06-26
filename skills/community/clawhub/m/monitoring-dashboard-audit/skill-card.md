## Description: <br>
Monitoring infrastructure assessment covering Grafana dashboard analysis, PromQL query validation, alert rule evaluation, SLA/SLO reporting review, and Prometheus data source health checks for network operations environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and network operations teams use this skill to audit Grafana, Prometheus, and Alertmanager monitoring coverage, query quality, alerting behavior, SLA/SLO reporting, and data source health without modifying the target systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to Grafana, Prometheus, and Alertmanager data that may expose sensitive infrastructure details. <br>
Mitigation: Use it only with authorization, grant a dedicated read-only or Viewer-level token, and avoid admin credentials. <br>
Risk: Generated reports and command output may contain sensitive monitoring topology, service, alerting, and availability information. <br>
Mitigation: Handle audit outputs as sensitive infrastructure information and share them only with approved operations or security stakeholders. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/monitoring-dashboard-audit) <br>
- [CLI Reference - Grafana and Prometheus APIs](references/cli-reference.md) <br>
- [Query Reference - PromQL Patterns for Network Monitoring](references/query-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline API requests, shell commands, tables, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit findings, coverage scorecards, prioritized recommendations, and PromQL or alerting examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
