## Description: <br>
Extract structured data from PDF invoices and documents, including scanned PDFs through OCR and digital PDFs through text extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tktk-ai](https://clawhub.ai/user/tktk-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and data teams use this skill to extract invoice fields, line items, totals, and currency data from PDF invoices, receipts, and financial documents into structured exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice PDFs and exported CSV or JSON files may contain sensitive financial or personal data. <br>
Mitigation: Only process authorized documents, run the tool in an isolated environment, and store generated exports securely. <br>
Risk: OCR and regex-based parsing can misread invoice fields, totals, dates, or line items. <br>
Mitigation: Review extracted results before using them for accounting, payment, compliance, or customer-facing workflows. <br>
Risk: Scanned PDFs require OCR dependencies that may not be present in the runtime environment. <br>
Mitigation: Install Tesseract and the documented Python dependencies before processing scanned or image-based PDFs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tktk-ai/pdf-invoice-parser) <br>
- [Publisher profile](https://clawhub.ai/user/tktk-ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated scripts output CSV or JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process a single PDF or a directory of PDFs; OCR requires Tesseract and Python OCR dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
