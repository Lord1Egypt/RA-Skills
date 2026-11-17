## Description:

Centralized n8n hub for designing reliable flows (idempotency, retries, HITL) and operating them via the public REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to design reliable n8n workflows with idempotency, retries, logging, and review queues, and to operate workflows and executions through the n8n public REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through live n8n API operations using a powerful API key.

Mitigation: Use a least-privilege API key, provide it through environment injection or a secret manager, and review the skill before deployment.

Risk: Webhook tests, retries, deletes, role changes, credential updates, activations, deactivations, source-control actions, and bulk data operations can have real side effects.

Mitigation: Require explicit confirmation for high-impact actions and avoid production tests unless the side effects are understood.

## Reference(s):

- [n8n Public API Endpoint Index](assets/endpoints-api.md)
- [n8n Workflow Operations](assets/workflow-lab.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce workflow design specs by default and workflow.json plus a runbook on request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
