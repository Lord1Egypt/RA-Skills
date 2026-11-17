## Description:

Designs and outputs n8n workflow JSON with robust triggers, idempotency, error handling, logging, retries, and human-in-the-loop review queues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsjustfred](https://clawhub.ai/user/itsjustfred)

### License/Terms of Use:


## Use Case:

Developers, operations teams, and automation builders use this skill to design auditable n8n workflows with explicit triggers, data contracts, idempotency, logging, retries, error handling, and review queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflow JSON may behave incorrectly if imported without review.

Mitigation: Review generated workflows before importing them into n8n and keep workflows inactive until checked.

Risk: Workflow credentials or secrets could be exposed if entered directly into generated JSON.

Mitigation: Use credential names or environment-variable references instead of secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itsjustfred/skills/n8n-workflow-automation-1-0-0)
- [Runbook template](assets/runbook-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with optional n8n workflow JSON and runbook content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; generated workflow JSON should remain inactive until reviewed before import into n8n.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
