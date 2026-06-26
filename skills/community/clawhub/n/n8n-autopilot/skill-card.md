## Description: <br>
AI-powered n8n workflow builder and deployer that generates workflow JSON from natural language, validates structure and logic, and can deploy workflows to an n8n instance through the REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drfirass](https://clawhub.ai/user/drfirass) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to create, validate, inspect, optimize, deploy, activate, and monitor n8n workflows from natural-language requests or existing workflow JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, activate, run, inspect, and delete workflows on a real n8n instance. <br>
Mitigation: Use a staging instance or least-privileged n8n API key where possible, and require explicit approval before deploy, activate, run, or delete operations. <br>
Risk: Generated workflow JSON may perform unintended actions if deployed without review. <br>
Mitigation: Review generated workflow JSON, credentials, external endpoints, and activation state before pushing it to n8n. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/drfirass/n8n-autopilot) <br>
- [n8n AI Workflow Builder documentation](https://docs.n8n.io/advanced-ai/ai-workflow-builder/) <br>
- [n8n Node Catalog & Credential Mapping](artifact/node-catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate deployable n8n workflow JSON and n8n API administration commands that require N8N_API_KEY and N8N_BASE_URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
