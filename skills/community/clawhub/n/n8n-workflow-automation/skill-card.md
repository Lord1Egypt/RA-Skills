## Description: <br>
Designs and outputs n8n workflow JSON with robust triggers, idempotency, error handling, logging, retries, and human-in-the-loop review queues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KOwl64](https://clawhub.ai/user/KOwl64) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to design auditable n8n automations with clear triggers, data contracts, retries, logging, review queues, and failure notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated n8n JSON could send data to unintended destinations or log sensitive fields if imported without review. <br>
Mitigation: Review nodes, destinations, credentials, logged fields, retry behavior, and the review queue before importing any generated workflow JSON. <br>
Risk: Workflow automation can fail silently or duplicate records when retries and deduplication are not configured correctly. <br>
Mitigation: Use the skill's idempotency, audit logging, failure notification, and human review queue steps before activating the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KOwl64/n8n-workflow-automation) <br>
- [Runbook template](assets/runbook-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional importable n8n workflow JSON and runbook markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only by default; workflow JSON is produced only when explicitly requested and should reference credential names or environment variables instead of secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
