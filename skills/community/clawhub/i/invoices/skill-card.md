## Description: <br>
Capture, extract, and organize received invoices with automatic OCR, provider detection, and searchable archive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external professionals, and small-business operators use this skill to capture invoices from email, uploads, photos, PDFs, or trusted invoice portals, extract invoice fields, validate them, and maintain a searchable local archive for review and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice PDFs and extracted metadata may contain tax IDs, addresses, payment references, amounts, and long-retained business records. <br>
Mitigation: Protect ~/invoices with appropriate local permissions, backups, and access controls; redact personal data before sharing exports. <br>
Risk: Broad email monitoring or untrusted invoice portal URLs could collect or download unintended sensitive content. <br>
Mitigation: Use a dedicated invoice mailbox, folder, or label for automation, and provide only trusted invoice portal URLs. <br>
Risk: OCR, field extraction, provider detection, duplicate detection, or tax math may be incomplete or incorrect. <br>
Mitigation: Review low-confidence required fields, validation failures, duplicate alerts, and tax discrepancies before relying on the archive for accounting or tax filings. <br>


## Reference(s): <br>
- [Invoices ClawHub listing](https://clawhub.ai/ivangdavila/invoices) <br>
- [Invoice processing workflow](process.md) <br>
- [Invoice data extraction](extraction.md) <br>
- [Search and reporting](search.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with structured JSON metadata examples, local file paths, and report/export descriptions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Organizes invoice PDFs and extracted metadata under ~/invoices; may produce CSV summaries, ZIP archives, and status reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
