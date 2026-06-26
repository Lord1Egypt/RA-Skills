## Description: <br>
Kibana is a Maton-authenticated API integration that helps agents read and manage saved objects, dashboards, data views, spaces, alerts, Fleet resources, connectors/actions, security roles, and cases in a connected Kibana instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security teams use this skill to inspect and administer Kibana resources through the Maton API gateway. It is suited for observability, security, and search analytics workflows that require authenticated Kibana API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and a connected Kibana API key, so credentials could grant access to sensitive observability or security data. <br>
Mitigation: Use dedicated least-privilege Kibana credentials, keep MATON_API_KEY out of logs and shared prompts, prefer non-production connections for exploration, and remove unused connections. <br>
Risk: Write-capable Kibana API calls can create, update, or delete dashboards, saved objects, data views, spaces, alert rules, Fleet resources, roles, and cases. <br>
Mitigation: Default to read-only requests, retrieve and display target resources first, describe the intended effect, and require explicit user approval with exact resource identifiers before POST, PUT, or DELETE requests. <br>
Risk: Connector execution can trigger external side effects such as sending email, posting messages, or invoking webhooks. <br>
Mitigation: Do not execute connectors proactively; confirm the connector ID, action type, target, and full payload with the user before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/kibana) <br>
- [Maton homepage](https://maton.ai) <br>
- [Kibana REST API documentation](https://www.elastic.co/docs/api/doc/kibana/) <br>
- [Saved Objects API](https://www.elastic.co/guide/en/kibana/current/saved-objects-api.html) <br>
- [Alerting API](https://www.elastic.co/guide/en/kibana/current/alerting-apis.html) <br>
- [Fleet API](https://www.elastic.co/guide/en/fleet/current/fleet-apis.html) <br>
- [Maton Community](https://discord.com/invite/dBfFAcefs2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown with API paths, shell commands, Python and JavaScript examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and the MATON_API_KEY environment variable; generated API calls may read or modify resources in the connected Kibana instance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
