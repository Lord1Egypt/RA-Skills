## Description: <br>
Guides agents through Lark Base operations including table, field, record, view, analytics, formula, lookup, form, dashboard, workflow, and role-permission tasks using lark-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gu2003li](https://clawhub.ai/user/gu2003li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to locate, read, write, analyze, or administer Lark Base resources through lark-cli. It is intended for Base-specific workflows that require real resource IDs, user-scoped permissions, and careful confirmation before changing business data or permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad changes to Lark Base content, schema, roles, workflows, attachments, and integrations using the user's account permissions. <br>
Mitigation: Require explicit confirmation and review target Base, table, field, record, role, workflow IDs, and payloads before schema changes, deletes, role changes, bulk writes, attachment uploads, workflow enablement, or workflows that send data to third-party URLs. <br>
Risk: Incorrect query scope or pagination handling can produce misleading analytics or incomplete conclusions. <br>
Mitigation: Use Base-side filtering, sorting, grouping, aggregation, and documented query ranges for global conclusions, and do not treat a partial page as a complete dataset. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gu2003li/lark-base) <br>
- [Lark Base data analysis SOP](references/lark-base-data-analysis-sop.md) <br>
- [Lark Base data query guide](references/lark-base-data-query-guide.md) <br>
- [Lark Base field JSON](references/lark-base-field-json.md) <br>
- [Lark Base cell value](references/lark-base-cell-value.md) <br>
- [Formula field guide](references/formula-field-guide.md) <br>
- [Lookup field guide](references/lookup-field-guide.md) <br>
- [Lark Base dashboard guide](references/lark-base-dashboard.md) <br>
- [Lark Base workflow guide](references/lark-base-workflow-guide.md) <br>
- [Lark Base role guide](references/lark-base-role-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with lark-cli commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires lark-cli and operates within the user's Lark account permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
