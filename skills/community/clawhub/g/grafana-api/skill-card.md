## Description: <br>
Grafana API integration with managed authentication for reading and managing dashboards, data sources, folders, annotations, alerts, and teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and observability teams use this skill to inspect and manage Grafana dashboards, data sources, folders, annotations, teams, and alert rules through Maton's managed API gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Grafana API traffic through Maton and requires sensitive credentials. <br>
Mitigation: Install only if you trust Maton, use a dedicated least-privilege Grafana service account token, avoid admin tokens unless required, and revoke the connection when finished. <br>
Risk: Write-capable Grafana operations can create, update, or delete dashboards, data sources, folders, annotations, alerts, and teams. <br>
Mitigation: Default to read-only inspection, review each proposed change, and require explicit approval with specific resource identifiers before any POST, PUT, PATCH, or DELETE request. <br>
Risk: High-impact changes can affect monitoring and observability workflows. <br>
Mitigation: Verify the target resource and summarize consequences before deleting dashboards, modifying alert rules, changing data sources, or reorganizing folders. <br>


## Reference(s): <br>
- [Grafana skill listing on ClawHub](https://clawhub.ai/byungkyu/grafana-api) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and explicit user approval before write operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
