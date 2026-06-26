## Description: <br>
Manage n8n workflows and automations via API. Use when working with n8n workflows, executions, or automation tasks - listing workflows, activating/deactivating, checking execution status, manually triggering workflows, or debugging automation issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomasansems](https://clawhub.ai/user/thomasansems) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation operators use this skill to create, inspect, validate, execute, monitor, and optimize n8n workflows through CLI and Python API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-backed workflow commands can create, execute, activate, deactivate, or otherwise alter live n8n workflows and their connected systems. <br>
Mitigation: Use a staging n8n instance or least-privileged API key where possible, review workflows before execution, and avoid sensitive test data. <br>
Risk: Dry-run testing can still trigger live workflow execution and may send emails, call third-party APIs, alter databases, or interrupt business workflows. <br>
Mitigation: Treat dry-run commands as live operations, run them against controlled workflows, and verify downstream side effects before using production credentials. <br>


## Reference(s): <br>
- [n8n API Reference](references/api.md) <br>
- [n8n API Documentation](https://docs.n8n.io/api/) <br>
- [n8n Documentation](https://docs.n8n.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires N8N_API_KEY and N8N_BASE_URL for API-backed operations.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
