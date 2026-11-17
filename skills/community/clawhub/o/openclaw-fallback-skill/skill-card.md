## Description:

Automatically calls a configured cloud API when the local model's confidence is below a threshold or it fails to answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dream458268696](https://clawhub.ai/user/dream458268696)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to route low-confidence, empty, or failed local-model responses to a configured cloud model endpoint so an agent can return a fallback answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content may be sent to the configured cloud model endpoint more often than the skill description suggests.

Mitigation: Use only a trusted endpoint, avoid sensitive conversations until fallback behavior is fixed, and require clear logging or user/admin consent for remote transfers.

Risk: The package includes an API-key-shaped value.

Mitigation: Rotate or remove the packaged value before installation and supply secrets through trusted local configuration or secret management.

Risk: User metadata may be forwarded to the cloud model endpoint.

Mitigation: Remove or minimize metadata forwarding unless it is required and approved for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dream458268696/skills/openclaw-fallback-skill)
- [Installation and configuration notes](artifact/readme.md)

## Skill Output:

**Output Type(s):** [text, configuration, shell commands, guidance]

**Output Format:** [Plain text or Markdown guidance with configuration JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a replacement fallback response or an error message; setup requires API endpoint, key, model, threshold, retry, timeout, and streaming settings.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
