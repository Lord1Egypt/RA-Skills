## Description: <br>
Autonomous n8n workflow automation agent - create, debug, monitor and optimize n8n workflows via natural language using the REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samansalari](https://clawhub.ai/user/samansalari) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to create, inspect, debug, test, monitor, and update n8n workflows through the n8n REST API. It is especially suited for workflow operations involving AI/LangChain nodes, execution troubleshooting, credentials metadata checks, and reusable workflow templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read or modify workflows, executions, activation state, and credential metadata in an n8n instance. <br>
Mitigation: Use a dedicated least-privilege n8n API key, prefer staging before production, and require explicit approval for updates, runs, activation, deactivation, and deletion. <br>
Risk: Webhook, AI-memory, and LLM workflow designs can involve sensitive data or third-party processing. <br>
Mitigation: Review workflows for sensitive data exposure, third-party LLM processing, and retention before deployment. <br>
Risk: API keys or workflow credentials could be exposed if copied into workspace files or logs. <br>
Mitigation: Store secrets in n8n's credential system, avoid logging credential values, and never write API keys or passwords to project files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samansalari/n8n-ops) <br>
- [Project Homepage](https://github.com/samansalari/Openclaw-N8N) <br>
- [n8n REST API Reference](api-reference.md) <br>
- [n8n AI Workflow Patterns](ai-patterns.md) <br>
- [n8n Verified Node Type Catalog](node-catalog.md) <br>
- [n8n Workflow Templates](templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, and workflow JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose n8n REST API calls and workflow JSON that require human review before production changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
