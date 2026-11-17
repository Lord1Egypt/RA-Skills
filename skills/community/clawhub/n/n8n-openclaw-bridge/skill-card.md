## Description:

Connects an OpenClaw agent to n8n so it can create, trigger, manage, and monitor workflows through natural-language automation requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marlowne12](https://clawhub.ai/user/marlowne12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to let an OpenClaw agent create, trigger, monitor, and manage n8n workflows. It supports business automations such as lead alerts, content publishing, website monitoring, execution debugging, and webhook-based agent-to-workflow dispatch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent operate a live n8n instance with broad workflow control.

Mitigation: Use a scoped n8n API key, separate development and production instances where possible, and pin the package version before use.

Risk: Workflow deletion, activation, deactivation, execution retry, and production webhook triggers can affect real automations.

Mitigation: Require human confirmation before these actions and review workflow changes before applying them to production.

Risk: n8n API URLs, API keys, and webhook URLs may be exposed if stored in broadly readable agent files.

Mitigation: Store secrets in environment variables or a secret manager and avoid placing credentials in shared plaintext files.

Risk: Included webhook templates may be unsafe if exposed without request authentication or payload validation.

Mitigation: Add webhook authentication, schema validation, and rate limiting before exposing workflows beyond a trusted environment.

## Reference(s):

- [N8n Openclaw Bridge on ClawHub](https://clawhub.ai/marlowne12/skills/n8n-openclaw-bridge)
- [n8n](https://n8n.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON workflow templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable n8n workflow JSON templates and API request examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
