## Description: <br>
Extract text from PDF files with automatic OCR fallback for scanned or image-based PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panpeter2024](https://clawhub.ai/user/panpeter2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract readable text from PDFs on disk when injected PDF text is missing, empty, garbled, truncated, or when OCR is needed for scanned documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional --auto-install flag can install OCR and PDF utilities on the host. <br>
Mitigation: Preinstall poppler and tesseract where possible, and use --auto-install only on hosts where package-manager changes are approved. <br>
Risk: The output option can replace an existing file at the selected path. <br>
Mitigation: Write extracted text to a new temporary or workspace path intended for this extraction. <br>
Risk: OCR output quality can degrade for low-resolution, handwritten, encrypted, password-protected, or image-heavy PDFs. <br>
Mitigation: Review extracted text before relying on it for downstream decisions, and obtain an unlocked or higher-quality source document when extraction is incomplete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panpeter2024/pdf-reader) <br>
- [Publisher profile](https://clawhub.ai/user/panpeter2024) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text extracted from PDFs, optionally saved to a text file, with shell command guidance for running the extractor.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses pdftotext for text-layer PDFs and Tesseract OCR fallback for scanned PDFs; configurable language and DPI options.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
