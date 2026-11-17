## Description:

Checks Apache Doris SQL syntax and conventions offline and returns a Markdown report with findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to review Apache Doris SQL syntax and coding conventions before execution. Treat its findings as advisory because incomplete SQL can pass validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can report incomplete SQL as passing.

Mitigation: Use the report as a preliminary lint result; verify SQL against the target Doris version and review it before execution.

Risk: Reports reproduce the submitted SQL, which may contain sensitive values.

Mitigation: Remove credentials and redact sensitive literals before generating or sharing reports.

Risk: Separately requested live profiling can affect database resources.

Mitigation: Run live profiling only with explicit authorization and database-side limits.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-doris-sql-check)
- [Doris SQL AST Schema](references/ast_schema.md)
- [Syntax Rules](rules/syntax_rules.yaml)
- [Specification Rules](rules/spec_rules.yaml)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown report containing SQL check findings and the submitted SQL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline advisory analysis; the report reproduces the submitted SQL.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
