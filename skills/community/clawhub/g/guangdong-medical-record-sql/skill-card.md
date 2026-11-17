## Description:

Generates and explains SQL queries for the Guangdong Medical Record Statistical Management System across outpatient, inpatient, emergency, surgery, ICD coding, and reporting scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangnan](https://clawhub.ai/user/liangnan)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare data analysts, hospital IT staff, and authorized database users can use this skill to draft SQL for Guangdong medical-record tables and build statistics for outpatient, inpatient, ICD, surgery, quality-control, and hospital report workflows.

### Deployment Geography for Use:

China (Guangdong Province)

## Known Risks and Mitigations:

Risk: The skill can generate queries against identifiable hospital and medical-record data.

Mitigation: Use only in authorized healthcare database environments; default to de-identified or aggregated outputs and mask direct identifiers unless specifically approved.

Risk: Broad patient or interface-table queries can expose more data than is necessary for the task.

Mitigation: Require minimum-necessary filters, approved time ranges, normal access controls, and audit logging before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangnan/skills/guangdong-medical-record-sql)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with SQL code blocks, table references, and concise query guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SQL examples, schema lookup guidance, field naming notes, and query-safety constraints.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
