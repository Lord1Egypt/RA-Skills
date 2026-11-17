## Description:

Production-ready n8n workflow templates for AI agents that deploy pre-built automations for webhooks, RSS monitoring, health checks, social metrics, and data backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoder-bawt](https://clawhub.ai/user/yoder-bawt)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation teams use this skill to deploy and manage n8n workflow templates for notifications, monitoring, metrics collection, and backups through an n8n instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review reports a local code-injection flaw in deploy.sh.

Mitigation: Review and patch deploy.sh before use, especially handling of template path and workflow name values passed into Python.

Risk: The server security review reports an unauthenticated Telegram-forwarding webhook template.

Mitigation: Add webhook authentication and payload validation before exposing or activating the webhook workflow.

Risk: The workflows require n8n API, Telegram, social API, backup, and execution-history configuration that may affect sensitive systems or credentials.

Mitigation: Use a minimally privileged n8n API key and review each workflow's credentials, destinations, and retention settings before activation.

## Reference(s):

- [n8n Documentation](https://docs.n8n.io/)
- [n8n API Reference](https://docs.n8n.io/api/)
- [n8n Workflow Examples](https://n8n.io/workflows/)
- [ClawHub Skill Page](https://clawhub.ai/yoder-bawt/skills/n8n-workflow-templates)
- [Publisher Profile](https://clawhub.ai/user/yoder-bawt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and workflow JSON references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, bash, N8N_HOST, and N8N_API_KEY; workflows must be customized with service credentials before activation.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
