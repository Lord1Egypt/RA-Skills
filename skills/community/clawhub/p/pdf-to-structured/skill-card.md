## Description:

Extract structured data from construction PDFs. Convert specifications, BOMs, schedules, and reports from PDF to Excel/CSV/JSON. Use OCR for scanned documents and pdfplumber for native PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and construction data teams use this skill to extract tables and text from native or scanned construction PDFs and structure them for analysis or integration. It supports specifications, bills of materials, schedules, reports, and submittals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation can introduce ordinary package supply-chain and environment-change risks.

Mitigation: Use a virtual environment and review or pin dependency versions before installing PDF and OCR packages.

Risk: Extracted spreadsheets, CSV files, JSON files, or text may contain confidential PDF content.

Mitigation: Store extracted outputs only in approved secure locations and apply the same handling controls as the source PDFs.

Risk: Cloud OCR services may expose confidential documents outside the local environment.

Mitigation: Prefer local Tesseract OCR for confidential PDFs and require explicit user approval before using any cloud OCR service.

Risk: PDF table extraction and OCR can produce incomplete or low-confidence structured data.

Mitigation: Review confidence scores, warnings, and source page references before relying on extracted data.

## Reference(s):

- [Pdf To Structured Skill Page](https://clawhub.ai/datadrivenconstruction/skills/pdf-to-structured)
- [Data-Driven Construction](https://datadrivenconstruction.io)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell code blocks; generated data files may be Excel, CSV, JSON, JSON Lines, or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include extraction confidence, low-confidence warnings, and source page references for extracted items.]

## Skill Version(s):

2.0.0 (source: artifact/claw.json and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
