## Description:

Paper Analyzer helps an agent read academic papers, extract twelve structured research-reading elements, and save the analysis as an Excel report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yipng05-max](https://clawhub.ai/user/yipng05-max)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and analysts use this skill to convert one or more academic papers into a structured twelve-dimension reading analysis, with concise Markdown results and an Excel workbook for review or comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted paper-derived text may be written into spreadsheet cells in a form interpreted as formulas.

Mitigation: Escape spreadsheet formula prefixes before writing paper text into Excel cells.

Risk: Temporary JSON used during export may remain on disk after the workbook is generated.

Mitigation: Delete temporary JSON files after export completes.

Risk: Excel output saved in the source-paper folder may overwrite an existing file.

Mitigation: Ask before overwriting existing files or choose a unique output path.

Risk: Externally supplied papers may contain hostile or misleading content.

Mitigation: Review the extracted analysis before relying on it, especially for untrusted papers.

## Reference(s):

- [12 Reading Elements](references/reading_elements.md)
- [ClawHub Skill Page](https://clawhub.ai/yipng05-max/skills/paper-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files]

**Output Format:** [Markdown summary plus Excel workbook (.xlsx)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For multi-paper analysis, the Excel workbook includes per-paper worksheets and a cross-paper comparison worksheet.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
