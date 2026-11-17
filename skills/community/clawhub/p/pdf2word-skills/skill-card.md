## Description:

Convert scanned PDF documents into Word text documents using a free, local OCR engine or remote API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottkiss](https://clawhub.ai/user/scottkiss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing users use this skill to convert scanned PDF files into editable Word documents with a local OCR engine, with optional remote OCR when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install workflow downloads and runs a third-party OCR executable without built-in checksum verification.

Mitigation: Install only after reviewing the download source and validating the executable through an independent integrity check.

Risk: Using the optional Gemini OCR engine may send document contents to a remote provider.

Mitigation: Use the default local engine for confidential PDFs, and use remote OCR only when the document handling policy allows it.

Risk: The optional Gemini API key may be stored in a local configuration file.

Mitigation: Store API keys with owner-only permissions or in an approved secret manager.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottkiss/skills/pdf2word-skills)
- [Simplified Chinese README](README_zh.md)
- [docr release download location](https://github.com/scottkiss/doc-ocr/releases/download/$VERSION/$FILENAME)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions, bash commands, and generated .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires input PDF and output .docx paths; accepts optional docr arguments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
