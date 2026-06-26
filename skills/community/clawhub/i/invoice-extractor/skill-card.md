## Description: <br>
Extracts invoice information from image and PDF files using Baidu OCR API and exports the results to Excel, with support for single-file, multi-file, directory, and batch processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aitanjp](https://clawhub.ai/user/aitanjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to process invoices or receipts from images and PDFs, extract buyer, seller, item, and amount fields, and generate Excel workbooks for accounting or review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports live-looking Baidu credentials in documentation. <br>
Mitigation: Do not use included example keys; create separate Baidu credentials, store them securely, and rotate any credentials copied from the documentation. <br>
Risk: Invoice files may contain sensitive business, tax, or personal data that is sent to a third-party OCR service. <br>
Mitigation: Process only invoices the user is authorized to send to Baidu Cloud OCR and confirm organizational privacy requirements before batch processing. <br>
Risk: Batch directory processing can include unintended files. <br>
Mitigation: Use preview/list mode before running batch jobs and avoid broad directories that may contain unrelated sensitive files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aitanjp/invoice-extractor) <br>
- [Baidu Cloud OCR Product](https://cloud.baidu.com/product/ocr) <br>
- [Baidu OCR API Documentation](https://cloud.baidu.com/doc/OCR/index.html) <br>
- [Baidu VAT Invoice OCR Endpoint](https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and generated Excel files from the skill runtime] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Baidu OCR credentials and produces Excel workbooks containing extracted invoice data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
