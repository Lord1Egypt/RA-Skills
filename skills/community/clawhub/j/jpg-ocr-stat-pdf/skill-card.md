## Description:

Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging and splitting documents, and handling forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agents use this skill to inspect, generate, transform, split, merge, repair, OCR, and fill PDF documents. It is especially useful for workflows that need structured extraction, form-field discovery, validation images, or scripted PDF output files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs may contain sensitive or restricted information.

Mitigation: Use this skill only with PDFs the user is authorized to process, and keep generated intermediate files in an appropriate workspace.

Risk: Password-protected PDF commands can expose secrets in command history or logs.

Mitigation: Avoid placing real passwords directly in shell commands when possible; use safer secret handling supported by the environment or tool.

Risk: Unpinned package installs can produce inconsistent behavior across environments.

Mitigation: Use a virtual environment with pinned dependencies before running PDF-processing examples or helper scripts.

Risk: PDF repair, fill, split, merge, and conversion workflows can overwrite or replace important documents.

Mitigation: Write repaired, filled, or converted PDFs to new output files and retain original source documents.

Risk: Form-filling coordinates or inferred field meanings can be inaccurate for non-fillable PDFs.

Mitigation: Create and inspect validation images, check bounding boxes, and verify the final filled PDF before relying on it.

## Reference(s):

- [PDF Processing Guide](artifact/SKILL.md)
- [PDF Forms Guide](artifact/forms.md)
- [PDF Processing Advanced Reference](artifact/reference.md)
- [Adobe PDF 32000-1:2008 Reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448)
- [ClawHub Skill Page](https://clawhub.ai/wu-uk/skills/jpg-ocr-stat-pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; helper scripts can produce PDF, PNG, JSON, text, table, or spreadsheet files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file outputs depend on the selected PDF operation and should be written to explicit output paths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
