## Description:

Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and document-automation users use this skill to analyze, transform, generate, split, merge, OCR, and fill PDF documents with Python libraries, command-line tools, and local helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDFs may contain sensitive document content, and the skill can create local intermediate PNG, JSON, text, and PDF files.

Mitigation: Use a private working directory for sensitive documents and delete intermediate files when the task is complete.

Risk: Examples include decrypting password-protected PDFs.

Mitigation: Only decrypt PDFs when authorized and handle passwords according to the user's security policy.

Risk: Repair or in-place modification commands can change or overwrite source documents.

Mitigation: Work from backups or copies before running repair, replacement, or form-filling commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/latex-formula-extraction-pdf)
- [PDF forms guide](artifact/forms.md)
- [PDF processing advanced reference](artifact/reference.md)
- [PDF 32000-1:2008 field state reference](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf#page=448)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets plus local JSON, PNG, text, and PDF file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local helper scripts may create intermediate images, JSON field maps, extracted text, and modified PDF files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
