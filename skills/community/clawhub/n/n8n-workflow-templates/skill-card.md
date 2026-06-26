## Description: <br>
Production-ready n8n workflow templates for AI agents that deploy pre-built automations for webhooks, RSS monitoring, health checks, social metrics, and data backup with workflow management utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoder-bawt](https://clawhub.ai/user/yoder-bawt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use this skill to deploy reusable n8n workflow templates and manage workflows through the n8n API. It supports common automation scenarios such as webhooks, RSS monitoring, health checks, social metrics collection, and data backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a command-injection weakness in the deploy helper when untrusted template paths or workflow names are used. <br>
Mitigation: Use only trusted local template files and workflow names, review deploy inputs before execution, and avoid passing untrusted values to deploy.sh. <br>
Risk: The skill uses an n8n API key with broad workflow-management authority. <br>
Mitigation: Use a least-privilege n8n API key where possible, keep it out of logs and shell history, and rotate it if exposure is suspected. <br>
Risk: Workflow activation, deletion, backup, and deployment operations can affect production automations or data. <br>
Mitigation: Review each workflow before activation and test backup, delete, and deployment operations outside production first. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yoder-bawt/n8n-workflow-templates) <br>
- [Publisher profile](https://clawhub.ai/user/yoder-bawt) <br>
- [Publisher homepage](https://github.com/yoder-bawt) <br>
- [n8n Documentation](https://docs.n8n.io/) <br>
- [n8n API Reference](https://docs.n8n.io/api/) <br>
- [n8n Workflow Examples](https://n8n.io/workflows/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and n8n workflow JSON templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, N8N_HOST, and N8N_API_KEY; generated workflows should be reviewed before activation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
