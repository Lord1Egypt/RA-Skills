## Description:

Extract Chinese and English text from images and scanned PDFs, including documents like invoices and contracts, using PaddleOCR in Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roamer-remote](https://clawhub.ai/user/roamer-remote)

### License/Terms of Use:


## Use Case:

Developers and document-processing users use this skill to extract text from scanned PDFs, images, invoices, contracts, and multi-page documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned package installation can change dependency behavior or introduce unreviewed code.

Mitigation: Use a pinned, reviewed requirements file or a controlled package source before installation.

Risk: PDF processing writes temporary images to shared paths, which can expose sensitive document content on shared machines.

Mitigation: Use a private per-run temporary directory and avoid processing sensitive PDFs on shared machines until temporary-file handling is fixed.

Risk: The OCR script initializes PaddleOCR with Chinese language settings, which may affect expected behavior for other languages.

Mitigation: Make the OCR language setting configurable and verify results for the intended document languages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roamer-remote/skills/ocr-python)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; OCR script output is plain text and recognized text data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recognition may include text strings and confidence scores when using PaddleOCR result data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
