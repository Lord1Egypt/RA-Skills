## Description:

Autonomous n8n workflow automation agent that helps create, debug, monitor, and optimize n8n workflows via natural language and the REST API, including AI/LangChain pipelines, execution monitoring, credential management, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samansalari](https://clawhub.ai/user/samansalari)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to create, inspect, debug, test, monitor, and optimize n8n workflows through the n8n REST API and workflow JSON. It supports AI/LangChain workflow patterns, execution analysis, credential setup guidance, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad workflow-control powers over n8n workflows, executions, and credential metadata.

Mitigation: Use a dedicated, least-privilege n8n API key, prefer a staging instance first, and confirm exact workflow IDs and expected side effects before run, delete, activate, deactivate, or test actions.

Risk: Templates can run workflows, send data to external services, and share AI memory by default.

Mitigation: Review OpenAI, Slack, webhook, HTTP Request, credential, and memory nodes before deployment; replace the shared `default` memory fallback with authenticated per-user session keys and avoid sending sensitive webhook payloads to third-party services unless intended.

## Reference(s):

- [n8n ops ClawHub page](https://clawhub.ai/samansalari/skills/n8n-ops)
- [Openclaw-N8N homepage](https://github.com/samansalari/Openclaw-N8N)
- [n8n REST API Reference](artifact/api-reference.md)
- [n8n Verified Node Type Catalog](artifact/node-catalog.md)
- [n8n AI Workflow Patterns](artifact/ai-patterns.md)
- [n8n Workflow Templates](artifact/templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include n8n workflow JSON, curl API calls, validation notes, diffs, and deployment guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
