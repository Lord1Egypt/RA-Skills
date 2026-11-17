## Description:

金蝶EAS Cloud ERP系统数据库SQL查询技能，支持采购、销售、库存、财务等模块的单据查询和数据分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxy-99](https://clawhub.ai/user/fxy-99)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized analysts, operators, and developers use this skill to inspect Kingdee EAS Cloud ERP PostgreSQL tables and draft SQL for sales orders, purchasing, inventory, accounts payable, accounts receivable, and finance reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact exposes direct credentials and connection details for a specific ERP database.

Mitigation: Install or use the skill only with explicit authorization, and rotate or replace the exposed credential with a managed secret before any deployment.

Risk: Arbitrary SQL and schema-enumeration queries could expose confidential ERP data or affect production database performance.

Mitigation: Use a strictly read-only, allowlisted database role; limit execution to approved audit or reporting workflows; and keep date filters and row limits on large-table queries.

Risk: ERP query results may be misread if table mappings, status codes, or business rules differ from the documented examples.

Mitigation: Validate table and field mappings with the system owner before relying on outputs for operational or financial decisions.

## Reference(s):

- [金蝶ERP常用表清单](artifact/references/tables.md)
- [ClawHub skill page](https://clawhub.ai/fxy-99/skills/kingdee-sold)
- [Publisher profile](https://clawhub.ai/user/fxy-99)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with SQL, Python, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include database query examples, table descriptions, troubleshooting guidance, and JSON-formatted query results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
