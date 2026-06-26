## Description: <br>
Designs and outputs n8n workflow JSON with robust triggers, idempotency, error handling, logging, retries, and human-in-the-loop review queues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to design auditable n8n workflows that define triggers, data contracts, idempotency, logging, retries, and human review queues before importing or operating them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workflow JSON could automate actions against external systems before it has been reviewed. <br>
Mitigation: Keep generated n8n workflows inactive until reviewed, validate the JSON before import, and confirm triggers, destinations, and success criteria. <br>
Risk: Workflow credentials or logs could expose sensitive data if over-scoped or recorded directly. <br>
Mitigation: Use least-privilege credentials, reference credential names or environment variables instead of secrets, and avoid logging unnecessary sensitive data. <br>
Risk: Failed or retried workflow runs could duplicate records or silently drop work. <br>
Mitigation: Define deduplication keys, add audit logging and failure notifications, and route failures to a human review queue. <br>


## Reference(s): <br>
- [n8n Workflow Runbook Template](assets/runbook-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown with optional n8n workflow JSON and runbook Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflow JSON is inactive by default and should reference credential names or environment variables instead of secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
