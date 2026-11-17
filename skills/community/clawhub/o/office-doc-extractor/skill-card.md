## Description:

Convert Microsoft Office documents (DOCX, XLSX, PPTX) to Markdown without external dependencies for analysis, indexing, or LLM processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators use this skill to convert DOCX, XLSX, and PPTX files into Markdown for review, indexing, summarization, or downstream LLM workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large, malformed, or malicious Office files may cause excessive resource use during ZIP and XML parsing.

Mitigation: Process untrusted or bulk document uploads in a constrained environment and apply file size, decompression, timeout, and output limits before conversion.

Risk: The converter extracts text and basic structure only, so images, embedded objects, complex formatting, encrypted files, and OCR needs may be omitted.

Mitigation: Confirm converted Markdown against the source document when complete fidelity is required, and use a dedicated OCR or secure document-processing workflow for unsupported content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michealxie001/skills/office-doc-extractor)
- [openpyxl documentation](https://openpyxl.readthedocs.io)
- [et_xmlfile project](https://foss.heptapod.net/openpyxl/et_xmlfile)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown files and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-file and batch conversion; extracts text only and does not perform OCR.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
