## Description:

Designs and outputs n8n workflow JSON with robust triggers, idempotency, error handling, logging, retries, and human-in-the-loop review queues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to design auditable n8n automations with schedules or webhooks, idempotent processing, status logging, retries, and review queues for failed or privileged actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflow JSON may target unintended APIs, destinations, schedules, or credential names.

Mitigation: Review each generated n8n workflow before installation and confirm the APIs, destinations, schedules, and credential references match the intended automation.

Risk: Secrets could be exposed if pasted directly into workflow JSON.

Mitigation: Use scoped n8n credentials or environment variables and keep secrets out of generated workflow files.

Risk: Privileged workflow actions could run without sufficient human oversight.

Mitigation: Keep human approval steps and review queues for privileged actions or failed-item reprocessing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/n8n-workflow-automation-litiao)
- [Runbook template](assets/runbook-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance, workflow design specifications, and optional n8n importable JSON plus runbook Markdown when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; workflow JSON should reference scoped n8n credentials or environment variables rather than embedding secrets.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
