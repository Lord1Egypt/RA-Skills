## Description: <br>
Extract structured data from construction PDFs, including specifications, bills of materials, schedules, and reports, into Excel, CSV, or JSON using pdfplumber and optional OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbmoradi60](https://clawhub.ai/user/dbmoradi60) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and construction data engineers use this skill to plan and generate PDF extraction workflows for native and scanned construction documents. It provides examples for extracting tables, text, bills of materials, schedules, specifications, and batch outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF extraction examples can save document contents into local Excel, CSV, JSON, JSONL, or text files. <br>
Mitigation: Run the workflow only on PDFs whose contents are appropriate to store in local output files. <br>
Risk: Package provenance is unavailable for this release. <br>
Mitigation: Verify the package identity before use when provenance is important. <br>
Risk: OCR and table extraction quality can vary with scanned-document quality and PDF layout. <br>
Mitigation: Review extracted outputs before relying on them, and adjust DPI, OCR language, or table settings when results are incomplete. <br>


## Reference(s): <br>
- [Data Driven Construction](https://datadrivenconstruction.io) <br>
- [pdfplumber documentation](https://github.com/jsvine/pdfplumber) <br>
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples may write extracted PDF content to local Excel, CSV, JSON, JSONL, or text files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
