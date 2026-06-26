## Description: <br>
Grafana HTTP API integration. Inspect dashboards, folders, data sources, alert rules, and teams. Use this skill when users want to query observability data, inspect monitoring resources, or manage Grafana dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations teams use this skill to inspect and manage Grafana dashboards, folders, data sources, alert rules, teams, and organization resources from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Grafana resources through configured ClawLink credentials. <br>
Mitigation: Use a least-privilege Grafana API key or service account scoped to the resources the agent needs. <br>
Risk: Write or destructive Grafana operations can create, update, or delete dashboards, folders, data sources, alert rules, teams, or permissions. <br>
Mitigation: Review write previews carefully and require explicit user confirmation before executing create, update, or delete actions. <br>
Risk: Admin-level Grafana credentials could expose broad organization, user, data source, team, permission, and alert-management capabilities. <br>
Mitigation: Avoid Grafana admin credentials unless those capabilities are required for the intended deployment. <br>


## Reference(s): <br>
- [Grafana HTTP API Documentation](https://grafana.com/docs/grafana/latest/developers/http_api/) <br>
- [Grafana Dashboard API](https://grafana.com/docs/grafana/latest/developers/http_api/dashboard/) <br>
- [Grafana Alerting API](https://grafana.com/docs/grafana/latest/developers/http_api/alerting/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=grafana-monitoring) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live Grafana tool catalogs where available; write actions require explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
