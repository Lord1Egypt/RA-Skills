## Description:

Extract table content from images, retrieve row/column data, correct recognition errors, and generate a well-formatted Excel file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to convert uploaded images containing tables into corrected row and column data, then save the result as a formatted Excel workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented shell workflow passes extracted JSON as a command argument, which can create avoidable command-execution and quoting risks.

Mitigation: Pass table data through stdin or an argument-vector API and validate the parsed JSON before workbook generation.

Risk: The helper script attempts to install openpyxl automatically at runtime.

Mitigation: Declare openpyxl as a pinned dependency and install it during packaging or deployment instead of from the running script.

Risk: The script accepts arbitrary output paths and does not document overwrite behavior.

Mitigation: Restrict writes to an approved workspace directory and document or prevent overwrites before saving workbooks.

Risk: OCR-derived cell values may include formula-like strings that spreadsheet software could evaluate.

Mitigation: Neutralize formula-like values before writing cells to the workbook.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/image-to-excel)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands]

**Output Format:** [Markdown response with a saved .xlsx file path and a preview of extracted rows; helper script writes an Excel workbook.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces .xlsx workbooks from corrected 2D JSON array data and previews the first five extracted rows.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
