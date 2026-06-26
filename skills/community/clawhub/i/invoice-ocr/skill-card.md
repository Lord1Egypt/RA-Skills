## Description: <br>
Recognizes VAT invoice content from PDFs or common image formats, sends the selected files to Baidu Cloud OCR for field extraction, and produces a structured Excel report with quality scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengyulong](https://clawhub.ai/user/pengyulong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to extract structured fields from VAT invoice PDFs or images, batch-process invoices, and create Excel summaries for review. It is suited to workflows that need invoice detection, OCR extraction, and a basic quality assessment before human validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected invoice PDFs or images are sent to Baidu Cloud OCR for processing. <br>
Mitigation: Process only files the user has approved for external OCR, and disclose the Baidu Cloud dependency before running the skill. <br>
Risk: Baidu API credentials are read from a local .env file. <br>
Mitigation: Use dedicated credentials, keep the .env file private, and avoid committing or sharing credential files. <br>
Risk: The documented dependency command installs packages system-wide with --break-system-packages. <br>
Mitigation: Prefer a virtual environment with pinned dependencies before running the OCR script. <br>
Risk: OCR output may be incomplete or inaccurate for low-quality scans or non-standard invoices. <br>
Mitigation: Review low-scoring rows in the Excel report and manually verify key fields such as totals, invoice number, date, buyer, and seller. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pengyulong/invoice-ocr) <br>
- [Baidu Intelligent Cloud OCR console](https://console.bce.baidu.com/ai/#/ai/ocr/overview/index) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files, Text] <br>
**Output Format:** [Markdown guidance with bash commands plus a generated XLSX report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local invoice files, Baidu Cloud OCR credentials, and a user-confirmed Excel output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
