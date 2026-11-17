## Description:

Generate Office files with a bundled Python engine. Use when creating or exporting Word (.docx), Excel (.xlsx), or PowerPoint (.pptx) files from structured JSON, reports, meeting minutes, project plans, trackers, business briefs, or natural-language requirements that must be turned into Office documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujohn74](https://clawhub.ai/user/lujohn74)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn structured JSON or natural-language document requirements into Word, Excel, or PowerPoint files for reports, meeting minutes, project plans, trackers, and business briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup downloads unpinned Python packages into the bundled environment.

Mitigation: Install and run the skill only in an isolated environment that the user trusts.

Risk: Spreadsheet cells generated from untrusted JSON may contain formula-like values.

Mitigation: Sanitize untrusted spreadsheet input before generating Excel files.

Risk: Generated Office files can overwrite existing files at the requested output path.

Mitigation: Choose output paths deliberately and check for existing files before generation.

## Reference(s):

- [Input formats](references/input-formats.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and generated Office document file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates .docx, .xlsx, or .pptx files from JSON requests or built-in business templates.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
