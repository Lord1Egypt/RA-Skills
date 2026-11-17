## Description:

OCR Locally helps an agent extract text from images and PDFs on macOS using local Vision and PDFKit-based Swift scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ltryee](https://clawhub.ai/user/ltryee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform offline OCR on user-selected images, screenshots, scanned documents, and PDFs on macOS. It supports plain-text extraction, optional confidence details, JSON output, language selection, and PDF page selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local image or PDF files and may write OCR output files.

Mitigation: Use only intended input files, choose explicit output paths, and avoid reusing filenames that contain important content.

Risk: Invalid PDF page ranges may crash or hang an OCR run.

Mitigation: Prefer simple validated page ranges such as 1-5 and use the dedicated PDF script for PDF files.

Risk: OCR output can be inaccurate, especially for low-confidence blocks or complex layouts.

Mitigation: Review confidence details and manually verify low-confidence or business-critical extracted text.

## Reference(s):

- [Usage Guide](references/usage.md)
- [Apple Vision Framework Documentation](https://developer.apple.com/documentation/vision)
- [VNRecognizeTextRequest Documentation](https://developer.apple.com/documentation/vision/vnrecognizetextrequest)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; OCR results are plain text, confidence text files, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on macOS 10.15+ and may write user-specified OCR output files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
