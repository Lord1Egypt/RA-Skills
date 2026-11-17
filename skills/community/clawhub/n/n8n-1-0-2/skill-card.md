## Description:

Manage n8n workflows and automations via API for listing workflows, activating or deactivating workflows, checking execution status, manually triggering workflows, and debugging automation issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pntrivedy](https://clawhub.ai/user/pntrivedy)

### License/Terms of Use:


## Use Case:

Developers and automation operators use this skill to inspect, operate, troubleshoot, and manually trigger n8n workflows through the n8n REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can activate, deactivate, delete, or manually execute n8n workflows, which may affect connected systems.

Mitigation: Require explicit human approval before any state-changing workflow action or manual execution.

Risk: The skill depends on an n8n API key and may encourage shell profile storage for credentials.

Mitigation: Use a least-privilege API key and avoid storing credentials in synced dotfiles when possible.

Risk: Commands send requests to the configured n8n base URL.

Mitigation: Configure only an HTTPS n8n base URL that the operator controls.

## Reference(s):

- [n8n API Reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON-formatted API responses when commands are executed against an n8n instance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
