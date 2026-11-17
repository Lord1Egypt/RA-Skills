## Description:

Audits an Odoo database's data quality with evidence before AI use, import, or migration, and guides remediation through odoo-mcp's gated write workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuanle96](https://clawhub.ai/user/tuanle96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to audit Odoo records for duplicates, missing required values, orphaned references, and format anomalies before trusting AI answers, importing data, or preparing migrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive Odoo data-quality evidence to the agent while auditing live records.

Mitigation: Use it only in Odoo environments approved for agent access and respect redacted fields without requesting broader field access.

Risk: Remediation batches could change incorrect records or values if approved without review.

Mitigation: Keep writes disabled unless required, inspect previewed record IDs and values, and confirm each gated write batch explicitly before execution.

Risk: Partial audits can mislead users when checks error or access limits hide records.

Mitigation: Report errored checks, diagnose access for orphaned references, and avoid presenting partial results as complete.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables, remediation plan, and per-model verdicts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes record-level evidence, proposed gated remediation batches, and before/after issue counts when remediation is run.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
