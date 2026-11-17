## Description:

Provides guidance for using lark-cli base commands to manage Lark Base tables, fields, records, views, analytics, formulas, lookup fields, forms, dashboards, workflows, roles, and permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gu2003li](https://clawhub.ai/user/gu2003li)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they need an agent to route, prepare, and review Lark Base operations through an authenticated lark-cli installation. It supports Base resource discovery, table and field management, record reads and writes, aggregation queries, forms, dashboards, workflows, and role or advanced permission tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide operations against live Lark Base data, roles, permissions, and workflows through lark-cli.

Mitigation: Review commands that update or delete records, change roles or advanced permissions, enable workflows, or upload and download attachments before execution.

Risk: Base data may be sent to external HTTP endpoints during workflow or integration tasks.

Mitigation: Use approved endpoints only and avoid sending unnecessary personal or business-sensitive fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gu2003li/skills/lark-base)
- [Base data analysis SOP](references/lark-base-data-analysis-sop.md)
- [Base data-query guide](references/lark-base-data-query-guide.md)
- [Base data-query DSL SSOT](references/lark-base-data-query.md)
- [Base CellValue specification](references/lark-base-cell-value.md)
- [Base field JSON SSOT](references/lark-base-field-json.md)
- [Base formula writing guide](references/formula-field-guide.md)
- [Base lookup field configuration guide](references/lookup-field-guide.md)
- [base +field-create](references/lark-base-field-create.md)
- [base +field-update](references/lark-base-field-update.md)
- [base +record-upsert](references/lark-base-record-upsert.md)
- [base +record-batch-create](references/lark-base-record-batch-create.md)
- [base +record-batch-update](references/lark-base-record-batch-update.md)
- [base +record-history-list](references/lark-base-record-history-list.md)
- [base +view-set-filter](references/lark-base-view-set-filter.md)
- [base +form-detail](references/lark-base-form-detail.md)
- [base +form-submit](references/lark-base-form-submit.md)
- [base +form-questions-create](references/lark-base-form-questions-create.md)
- [base +form-questions-update](references/lark-base-form-questions-update.md)
- [Dashboard module guide](references/lark-base-dashboard.md)
- [dashboard block data_config SSOT](references/dashboard-block-data-config.md)
- [base +dashboard-block-get-data](references/lark-base-dashboard-block-get-data.md)
- [Workflow guide](references/lark-base-workflow-guide.md)
- [Workflow steps JSON SSOT](references/lark-base-workflow-schema.md)
- [Base advanced permission and role guide](references/lark-base-role-guide.md)
- [Base role permission JSON SSOT](references/role-config.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated lark-cli installation and access to the target Lark Base resources.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog text report 1.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
