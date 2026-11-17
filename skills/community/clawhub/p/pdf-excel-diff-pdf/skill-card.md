## Description:

A PDF manipulation toolkit for extracting text and tables, creating, merging, splitting, modifying, and analyzing PDF documents, and handling fillable and non-fillable forms at scale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agents use this skill to process local PDFs, including text and table extraction, document generation, merge and split workflows, OCR preparation, and form completion. It supports both fillable PDF fields and non-fillable forms that require visual field analysis, bounding-box validation, and annotation-based output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated JSON, images, extracted text, and filled PDFs may contain sensitive information from the original document.

Mitigation: Store, transmit, or delete generated outputs according to the sensitivity of the source PDF and the user's data-handling requirements.

Risk: PDF modification, repair, or decryption workflows can alter documents or expose protected content.

Mitigation: Run examples on copies and use decryption or repair only for documents the user is authorized to process.

## Reference(s):

- [PDF form workflow](forms.md)
- [PDF processing advanced reference](reference.md)
- [Adobe PDF 32000-1:2008 standard](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Files]

**Output Format:** [Markdown guidance with inline Python, JavaScript, and shell code blocks; helper scripts produce JSON, PNG images, text annotations, and PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided PDF files and may create derivative document, image, text, and JSON outputs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
