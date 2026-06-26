## Description: <br>
Operate n8n via its public REST API from OpenClaw for workflow management, executions, and automation tasks across self-hosted n8n and n8n Cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation operators use this skill to inspect, configure, trigger, troubleshoot, and manage n8n workflows and related resources through the public REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real n8n workflows, executions, account resources, and webhooks when used with a powerful API key. <br>
Mitigation: Use a dedicated least-privileged API key, prefer test instances or test webhooks for experiments, and explicitly review activate, deactivate, retry, delete, transfer, role change, and webhook trigger actions before production use. <br>
Risk: API keys may be exposed if stored or copied into plain text configuration. <br>
Mitigation: Store credentials securely when possible and avoid committing or sharing N8N_API_KEY values. <br>


## Reference(s): <br>
- [n8n REST API Endpoint Reference](assets/n8n-api-endpoints.md) <br>
- [ClawHub skill page](https://clawhub.ai/codedao12/n8n-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses N8N_API_BASE_URL and N8N_API_KEY placeholders; production-changing actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
