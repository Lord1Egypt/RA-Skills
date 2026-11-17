## Description:

Extracts product model, quantity, price, currency, and image information from PDF quotations and product catalogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert supplier PDF quotations or product catalogs into structured product records for review, spreadsheet export, and image matching workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CSV or XLSX files may contain unsafe formula-like cells when the source PDF is untrusted.

Mitigation: Review or sanitize spreadsheet cells before opening generated files in spreadsheet software.

Risk: The skill writes extracted text, image, table, and spreadsheet outputs to user-selected paths.

Mitigation: Use a dedicated output directory and review generated files before sharing or importing them into other systems.

Risk: PDF layout variation can produce incomplete or mismatched product, price, quantity, or image extraction.

Mitigation: Run the PDF structure analysis first, confirm the currency with the user, and spot-check extracted records and matched images before relying on the output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/skills/newton-quotation-pdf-extraction)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python code blocks and local file outputs such as TXT, JSON, CSV, XLSX, and extracted images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are written to user-selected output paths; spreadsheet outputs should be reviewed before opening when source PDFs are untrusted.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
