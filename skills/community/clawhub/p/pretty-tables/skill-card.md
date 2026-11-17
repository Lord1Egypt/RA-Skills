## Description:

Pretty Tables helps agents create professional, full-width DOCX tables with the docx npm library that render consistently in Microsoft Word and Google Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happytreees](https://clawhub.ai/user/happytreees)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when generating JavaScript/docx code for itineraries, schedules, data tables, and reports that need consistent table width, shading, padding, and column sizing across DOCX viewers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated JavaScript examples may write DOCX files to disk in unintended locations.

Mitigation: Review output paths before running generated scripts and execute them only in intended project directories.

Risk: Changing the documented table-width, cell-width, shading, padding, or column-sum rules can produce inconsistent DOCX rendering across viewers.

Mitigation: Use DXA widths on both tables and cells, ShadingType.CLEAR for fills, explicit cell margins, and column widths that sum exactly to the table width.

## Reference(s):

- [ClawHub Pretty Tables skill page](https://clawhub.ai/happytreees/skills/pretty-tables)

## Skill Output:

**Output Type(s):** [guidance, code]

**Output Format:** [Markdown with JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes DXA table and cell widths, ShadingType.CLEAR fills, cell margins, and exact column-width sums.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
