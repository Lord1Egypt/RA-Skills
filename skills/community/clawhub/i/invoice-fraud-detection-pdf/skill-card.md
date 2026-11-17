## Description:

A PDF processing toolkit that helps agents extract text and tables, create, merge, split, analyze, and fill PDF documents and forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and document-processing agents use this skill to inspect, transform, extract from, and fill PDFs, including fillable and non-fillable forms. It is suited to workflows that need local PDF analysis, form-field mapping, validation images, annotations, or generated PDF outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF examples and helper scripts can modify or generate document files.

Mitigation: Use the skill in a normal project or scratch directory and keep backups before running workflows that alter PDFs.

Risk: PDF workflows may involve sensitive documents or passwords.

Mitigation: Avoid hardcoding real passwords in commands and handle source PDFs, extracted text, and generated files according to the user's data-handling requirements.

Risk: Optional Python dependencies are installed and executed locally.

Mitigation: Install optional dependencies in a virtual environment with reviewed versions when possible.

Risk: Manual bounding-box selection for non-fillable forms can place annotations incorrectly.

Mitigation: Use the provided validation-image and bounding-box checks, then visually inspect results before relying on a filled PDF.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/invoice-fraud-detection-pdf)
- [PDF form handling guide](artifact/forms.md)
- [PDF processing advanced reference](artifact/reference.md)
- [Adobe PDF 32000-1:2008 reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline Python, JavaScript, shell commands, and JSON schemas; helper scripts can produce JSON, PNG, and PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include modified PDFs, form-field JSON, validation images, extracted text, tables, or generated document files depending on the requested PDF workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
