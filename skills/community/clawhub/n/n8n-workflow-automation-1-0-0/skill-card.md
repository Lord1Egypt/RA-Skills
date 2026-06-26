## Description: <br>
Designs and outputs n8n workflow JSON with robust triggers, idempotency, error handling, logging, retries, and human-in-the-loop review queues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsjustFred](https://clawhub.ai/user/itsjustFred) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to design auditable n8n workflows with triggers, data contracts, idempotency, logging, retries, failure notifications, and human review queues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated n8n workflow JSON may perform unintended actions if imported or activated without review. <br>
Mitigation: Review generated workflow JSON before importing or activating it, and require human approval for workflows that touch production, customer, financial, or account data. <br>
Risk: Secrets could be exposed if credentials are placed directly in generated workflow files. <br>
Mitigation: Keep secrets in n8n credential storage or environment variables and reference credential names only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itsjustFred/n8n-workflow-automation-1-0-0) <br>
- [Runbook template](artifact/assets/runbook-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, code, guidance] <br>
**Output Format:** [Markdown with optional n8n workflow JSON and runbook content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated n8n workflow JSON is inactive by default and should reference credentials or environment variables rather than containing secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
