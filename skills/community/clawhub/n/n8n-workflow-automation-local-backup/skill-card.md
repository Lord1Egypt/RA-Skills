## Description: <br>
Designs and outputs n8n workflow JSON with robust triggers, idempotency, error handling, logging, retries, and human-in-the-loop review queues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[12357851](https://clawhub.ai/user/12357851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to design auditable n8n automations with clear triggers, data contracts, idempotency, retry behavior, logging, and human review queues. It can produce a workflow design spec by default, or importable workflow JSON and a runbook when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registry slug and bundled _meta.json slug do not fully match, which can cause package identity confusion. <br>
Mitigation: Verify the intended package name, publisher handle, and ClawHub skill page before installation or use. <br>
Risk: Generated n8n workflow JSON may connect to external systems or perform actions if imported and activated without review. <br>
Mitigation: Review generated workflow JSON before import, keep workflows inactive until checked, and use least-privilege credentials for connected services. <br>
Risk: Workflow designs that omit idempotency, logging, or failure routing can silently duplicate, drop, or mishandle records. <br>
Mitigation: Require deduplication keys, audit logging, retry limits, failure notifications, and a human review queue in generated workflow designs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/12357851/n8n-workflow-automation-local-backup) <br>
- [Runbook template](artifact/assets/runbook-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with optional n8n workflow JSON and runbook content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflow JSON is read-only by default, should reference credential names or environment variables instead of secrets, and should remain inactive until reviewed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
