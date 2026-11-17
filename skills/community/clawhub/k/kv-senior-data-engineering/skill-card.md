## Description:

Design and build scalable data pipelines, ETL/ELT systems, and data infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felix-antonio-sl](https://clawhub.ai/user/felix-antonio-sl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to design batch, streaming, and hybrid data pipelines; model warehouse data; add data quality controls; and troubleshoot pipeline or query performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workflow code or configuration may be unsafe or incorrect if deployed without review.

Mitigation: Review generated pipeline artifacts before deployment and add environment-specific tests, approvals, and rollback checks.

Risk: Untrusted YAML or JSON inputs could drive unintended generated pipeline behavior.

Mitigation: Use trusted configuration sources, validate inputs before generation, and avoid direct writes into production scheduler directories.

Risk: Sample credentials or destructive operations can create production exposure when copied into real pipelines.

Mitigation: Replace sample credentials with secret-managed values and require safeguards for truncate, backfill, rollback, and full-refresh operations.

## Reference(s):

- [Data Pipeline Architecture](references/data_pipeline_architecture.md)
- [Data Modeling Patterns](references/data_modeling_patterns.md)
- [DataOps Best Practices](references/dataops_best_practices.md)
- [Senior Data Engineer Workflows](references/workflows.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/felix-antonio-sl/skills/kv-senior-data-engineering)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually emits one primary artifact per response, such as a DAG, dbt model, schema DDL, quality rules, or architecture recommendation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
