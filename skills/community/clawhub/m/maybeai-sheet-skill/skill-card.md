## Description: <br>
Manages MaybeAI spreadsheets across upload, workbook profiling, read/write, worksheet operations, formulas, formula lineage tracing, formatting, and SQL result-table workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[no7dw](https://clawhub.ai/user/no7dw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and spreadsheet operators use this skill to profile, inspect, edit, format, share, and export MaybeAI spreadsheets, including SQL result sheets and formula lineage explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify spreadsheet contents and structure through write, row, column, worksheet, formula, and formatting operations. <br>
Mitigation: Use test workbooks first, require explicit user confirmation for destructive changes, and read back affected worksheets after writes. <br>
Risk: The bundled examples include export, sharing, public-link, editor-access, and delete workflows that can expose or remove sensitive workbook content. <br>
Mitigation: Remove or disable delete, share, and export steps before routine use, and require explicit confirmation before public links, editor grants, deletion, or sensitive exports. <br>
Risk: MaybeAI API access depends on MAYBEAI_API_TOKEN, so misuse of that token can affect workbooks available to the account. <br>
Mitigation: Install only when the MaybeAI service is trusted, keep the token scoped and protected, and verify workbook permissions before running scripts. <br>


## Reference(s): <br>
- [MaybeAI Sheet skill page](https://clawhub.ai/no7dw/maybeai-sheet-skill) <br>
- [MaybeAI repository homepage](https://github.com/OmniMCP-AI/maybeai-uni) <br>
- [File Management Reference](references/file-management.md) <br>
- [Read/Write Reference](references/read-write.md) <br>
- [Formulas and SQL Reference](references/formulas-sql.md) <br>
- [Workbook Profile Reference](references/workbook-profile.md) <br>
- [Formula Lineage Trace Reference](references/lineage-trace.md) <br>
- [Permission And Sharing Reference](references/permission-sharing.md) <br>
- [Errors and Recovery Reference](references/errors-recovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and API payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAYBEAI_API_TOKEN for MaybeAI API access.] <br>

## Skill Version(s): <br>
0.11.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
