## Description: <br>
Reviews multiple client Odoo databases through odoo-mcp cross-instance tools to summarize fleet accounting health, rank per-client aging issues, and triage partial failures for agencies and partners managing 5-50 instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuanle96](https://clawhub.ai/user/tuanle96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agencies, partners, and operators use this skill to answer portfolio-level questions across managed Odoo instances, identify unreachable or opted-out clients, compare per-client accounting metrics, and plan follow-up actions by client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can expose sensitive client accounting data across multiple managed Odoo instances. <br>
Mitigation: Install only where the configured odoo-mcp server is authorized to read the relevant client data, and keep per-client field ACLs and rate budgets in force. <br>
Risk: Opted-out clients could be unintentionally included or named in fleet-level results. <br>
Mitigation: Keep cross_instance disabled for opted-out clients and report only opted-out counts, not their data. <br>
Risk: Actions beyond read-only review could affect the wrong client if approvals are reused across instances. <br>
Mitigation: Route writes through the normal per-instance gate and never reuse approval tokens across clients. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tuanle96/skills/odoo-agency-fleet-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with per-client tables and grouped follow-up items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should retain _instance labels, reachable/unreachable/opted-out counts, redaction notices, and per-client grouping.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
