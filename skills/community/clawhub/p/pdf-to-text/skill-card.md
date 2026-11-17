## Description:

Extracts clean, readable text from PDF documents using the MinerU API and mineru-open-api CLI, including OCR support for scanned or image-based PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veeicwgy](https://clawhub.ai/user/veeicwgy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert native, scanned, or image-based PDF documents into plain text or Markdown for search, indexing, text mining, data processing, and NLP preprocessing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF content may be processed by a third-party service.

Mitigation: Use the skill only with PDFs approved for third-party processing.

Risk: Installing an unpinned global npm CLI can introduce supply-chain or privilege risk.

Mitigation: Prefer a pinned, local CLI installation and avoid running npm with elevated privileges.

Risk: Extracted text may persist in output directories after processing.

Mitigation: Choose an explicit output directory and clean it up after extraction.

## Reference(s):

- [MinerU API token management](https://mineru.net/apiManage/token)
- [ClawHub skill page](https://clawhub.ai/veeicwgy/skills/pdf-to-text)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown or plain text, with shell commands and optional output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports stdout output for quick extraction and output directories for saved, OCR, or batch extraction.]

## Skill Version(s):

0.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
