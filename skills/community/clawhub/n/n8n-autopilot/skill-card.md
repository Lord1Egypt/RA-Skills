## Description:

AI-powered n8n workflow builder and deployer that generates workflow JSON from natural language, validates structure and logic, and can deploy to an n8n instance via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drfirass](https://clawhub.ai/user/drfirass)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to draft, inspect, optimize, and optionally deploy n8n workflows from natural-language requirements or existing workflow JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change, activate, run, and delete live n8n workflows.

Mitigation: Prefer a staging n8n instance, require explicit confirmation before deploy, activate, run, or delete actions, and manually review generated workflow JSON first.

Risk: An n8n API key may grant broad access to modify the target instance.

Mitigation: Use a narrowly scoped and rotatable key, store it outside generated workflow content, and connect only to HTTPS N8N_BASE_URL values.

Risk: Generated or untrusted recipes may include risky nodes, credentials, schedules, webhooks, code, file transfer, SSH, commands, or outbound HTTP destinations.

Mitigation: Review node types, credentials, webhook exposure, schedules, code nodes, command and transfer nodes, and external destinations before import or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drfirass/skills/n8n-autopilot)
- [Publisher profile](https://clawhub.ai/user/drfirass)
- [n8n AI Workflow Builder documentation](https://docs.n8n.io/advanced-ai/ai-workflow-builder/)
- [n8n node catalog and credential mapping](artifact/node-catalog.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown containing n8n workflow JSON, node explanations, import instructions, and optional CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deployment operations require N8N_API_KEY and N8N_BASE_URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
