## Description:

Checks Spark SQL for Huawei Cloud MRS syntax, specification compliance, and potential performance risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use the skill to review one Spark SQL statement for MRS syntax issues, development specification violations, and potential performance risks before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can contain SQL snippets.

Mitigation: Provide only SQL you intend to review and keep generated reports private.

Risk: Static checks do not assess SQL injection, access control, or execution plans.

Mitigation: Review those concerns separately and treat the report as guidance rather than a replacement for security or execution-plan review.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-mrs-spark-sql-check)
- [AST Schema](artifact/references/ast-schema.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown report with a summary, findings, suggested fixes, and the submitted SQL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks only the first statement when input contains multiple SQL statements.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
