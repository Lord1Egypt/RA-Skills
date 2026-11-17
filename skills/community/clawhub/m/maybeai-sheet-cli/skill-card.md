## Description:

Guides agents in using the `mbs` CLI to inspect, import, edit, verify, export, and share MaybeAI spreadsheets across Sheet, Base, table, formula, SQL, chart, and file workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[no7dw](https://clawhub.ai/user/no7dw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and spreadsheet automation agents use this skill to plan and execute MaybeAI spreadsheet workflows with the `mbs` CLI, including target discovery, safe mutations, imports and exports, SQL materialization, chart or style operations, and sharing. It emphasizes runtime command discovery, dry runs, verification, and capability-gap reporting before destructive or unsupported actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to modify, delete, export, or share MaybeAI spreadsheet data when used with a valid API token.

Mitigation: Use a least-privilege token or account, review dry-run output before deletes or overwrites, and require explicit confirmation before making sheets public or granting editor access.

Risk: Commands based on stale command maps or hidden compatibility commands may fail or produce unsupported workflows.

Mitigation: Start with `mbs --help` and command-specific help, generate only public commands, and report capability gaps when current help does not support a request.

Risk: Spreadsheet imports, exports, and sharing operations may expose or transform sensitive workbook data.

Mitigation: Confirm source and target workbook identity, export destination, and sharing permissions before running; verify results with target-appropriate readback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/no7dw/skills/maybeai-sheet-cli)
- [MaybeAI Uni GitHub Homepage](https://github.com/OmniMCP-AI/maybeai-uni)
- [README](README.md)
- [CLI Command Reference](references/cli-commands.md)
- [Read/Write Reference](references/read-write.md)
- [File Management Reference](references/file-management.md)
- [Errors and Recovery Reference](references/errors-recovery.md)
- [Charts and Formatting Reference](references/charts-formatting.md)
- [Formulas and SQL Reference](references/formulas-sql.md)
- [Base Mode Verification Runbook](references/base-mode-verification.md)
- [Workbook Inspection Reference](references/workbook-profile.md)
- [Permission And Sharing Reference](references/permission-sharing.md)
- [Pivot Tables Reference](references/pivot-tables.md)
- [Engine Selection When Creating Data Products](references/engine-selection-when-create.md)
- [Formula Lineage and Computation Evidence](references/lineage-trace.md)
- [Maybe Sheet Clickable References](references/clickable-refs.md)
- [Sheet Worksheets With Multiple Tables](references/excelize-multiple-tables.md)
- [Legacy SQL Formula Showcase](references/sql-formula-showcase.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON/YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires `mbs` and `MAYBEAI_API_TOKEN`; recommends runtime help discovery, dry-run previews, and verification for mutations.]

## Skill Version(s):

v0.21.8 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
