## Description: <br>
Manage n8n workflows and automations via API for listing workflows, activating or deactivating them, checking execution status, manually triggering workflows, and debugging automation issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[droidhackzor](https://clawhub.ai/user/droidhackzor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to inspect, create, validate, execute, monitor, and optimize n8n workflows against an n8n instance through its REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger and change live n8n automations, including commands described as dry-run testing. <br>
Mitigation: Use a staging n8n instance or least-privilege API key where possible, review workflow JSON before creating or executing it, and treat tests as real workflow executions. <br>
Risk: The required n8n API key may allow management of live workflows and connected systems. <br>
Mitigation: Store credentials in OpenClaw settings or a secure secret manager, avoid shell startup files, and rotate or scope the API key according to the n8n environment. <br>


## Reference(s): <br>
- [n8n API Reference](references/api.md) <br>
- [n8n API documentation](https://docs.n8n.io/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON workflow or report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires N8N_API_KEY and N8N_BASE_URL to connect to an n8n instance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
