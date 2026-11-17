## Description:

Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging and splitting documents, and handling forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and agents use this skill to inspect, transform, generate, and repair PDFs, including extracting text and tables and working with fillable or non-fillable forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF processing can modify or repair source documents in ways that are difficult to reverse.

Mitigation: Use copies of PDFs for repair, form filling, merging, splitting, and annotation workflows before replacing original files.

Risk: PDF decryption examples could be misused on documents the user is not authorized to access.

Mitigation: Decrypt only PDFs that the user is authorized to access and retain the original encrypted file.

Risk: OCR workflows may require additional dependencies such as pytesseract and pdf2image.

Mitigation: Install OCR dependencies in a dedicated environment and review or pin package versions when possible.

Risk: Manual bounding boxes for non-fillable forms can place text in the wrong location.

Mitigation: Generate validation images, run the bounding-box checker, and visually inspect the results before writing the completed PDF.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnj22/skills/organize-messy-files-pdf)
- [PDF Processing Guide](artifact/SKILL.md)
- [PDF Form Handling Guide](artifact/forms.md)
- [PDF Processing Advanced Reference](artifact/reference.md)
- [Adobe PDF 32000-1:2008 Reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448)
- [pypdf FreeText annotation issue](https://github.com/py-pdf/pypdf/issues/2084)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, JSON field files, image validation artifacts, and PDF outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce extracted text or table data, generated or modified PDFs, form-field JSON, validation images, and repair or conversion commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
