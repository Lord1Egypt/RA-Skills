## Description:

Use MaybeAI Sheet CLI when an agent needs to inspect, import, edit, style, validate, refresh, export, or share MaybeAI spreadsheets through the mbs command-line interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[no7dw](https://clawhub.ai/user/no7dw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and spreadsheet automation agents use this skill to perform MaybeAI workbook, worksheet, table, formula, styling, dashboard, import/export, and sharing tasks through mbs while checking metadata before writes and verifying changes afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated mbs commands can edit, export, or share MaybeAI sheets using MAYBEAI_API_TOKEN.

Mitigation: Use a reviewed token in an isolated environment, inspect workbook metadata before writes, confirm doc IDs and worksheet names, and run --verify or readback checks after changes.

Risk: Sharing commands can expose workbooks more broadly than intended.

Mitigation: Check current permissions first and avoid public or editor sharing unless the user explicitly requests it.

Risk: Dashboard HTML can rely on external scripts that may be unsuitable for sensitive workbooks.

Mitigation: Use pinned, reviewed script sources and avoid unpinned external dashboard dependencies for sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/no7dw/skills/maybeai-sheet-cli-skill)
- [MaybeAI Uni homepage](https://github.com/OmniMCP-AI/maybeai-uni)
- [README](README.md)
- [CLI command catalog](references/cli-commands.md)
- [Read and write reference](references/read-write.md)
- [File management reference](references/file-management.md)
- [Charts and formatting reference](references/charts-formatting.md)
- [Formulas and SQL reference](references/formulas-sql.md)
- [Pivot tables reference](references/pivot-tables.md)
- [Permission and sharing reference](references/permission-sharing.md)
- [Errors and recovery reference](references/errors-recovery.md)
- [Workbook profile reference](references/workbook-profile.md)
- [Lineage trace reference](references/lineage-trace.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAYBEAI_API_TOKEN and an installed maybeai-sheet-cli mbs executable for execution.]

## Skill Version(s):

0.16.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
