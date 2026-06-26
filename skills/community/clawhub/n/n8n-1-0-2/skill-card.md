## Description: <br>
Manage n8n workflows and automations via API. Use when working with n8n workflows, executions, or automation tasks - listing workflows, activating/deactivating, checking execution status, manually triggering workflows, or debugging automation issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pntrivedy](https://clawhub.ai/user/pntrivedy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation operators use this skill to inspect, run, and manage n8n workflows and executions through the n8n REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate, deactivate, execute, or delete n8n workflows when given valid API credentials. <br>
Mitigation: Use a least-privileged n8n API key and manually review workflow IDs and payloads before running commands that change workflow state. <br>
Risk: The n8n API key is read from the user's shell environment. <br>
Mitigation: Keep the API key out of shared shell profiles and avoid exposing it in logs, prompts, screenshots, or shared terminals. <br>


## Reference(s): <br>
- [n8n API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires N8N_API_KEY and N8N_BASE_URL environment variables for live API access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
