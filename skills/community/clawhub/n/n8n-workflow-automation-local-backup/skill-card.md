## Description:

Designs and outputs n8n workflow JSON with robust triggers, idempotency, error handling, logging, retries, and human-in-the-loop review queues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[12357851](https://clawhub.ai/user/12357851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to design auditable n8n workflows with explicit triggers, data contracts, idempotency controls, retries, logging, failure notifications, and review queues. It can provide a design spec by default, or importable workflow JSON and a runbook when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflow JSON may create incorrect automation behavior or unintended actions if imported without review.

Mitigation: Review generated workflows before import, keep them inactive until tested, and verify triggers, data contracts, retries, and failure paths.

Risk: Workflow credentials or broad permissions could expose sensitive systems if embedded or over-scoped.

Mitigation: Use least-privilege credential names or environment references, avoid embedding secrets, and approve privileged access before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/12357851/skills/n8n-workflow-automation-local-backup)
- [Runbook Template](artifact/assets/runbook-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with optional n8n workflow JSON and runbook content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflow JSON should remain inactive by default and reference credential names or environment variables rather than embedding secrets.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
