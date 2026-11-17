## Description:

发票 OCR 识别技能，扫描文件夹中的 PDF、OFD 和图片发票，调用阿里云 OCR API 识别发票信息并导出 Excel 表格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[1054570699](https://clawhub.ai/user/1054570699)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers can use this skill to batch process invoice files for reimbursement, accounting, or invoice organization workflows. It helps an agent configure Alibaba Cloud OCR credentials, run invoice recognition, and produce a consolidated Excel spreadsheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice files may contain sensitive financial, tax, and identity information that is sent to Alibaba Cloud OCR for processing.

Mitigation: Use the skill only when that data transfer is acceptable, avoid processing unapproved confidential invoices, and review applicable privacy and compliance requirements before use.

Risk: Cloud AccessKey credentials are required and may be stored in the skill configuration file.

Mitigation: Do not paste cloud secrets into chat; configure credentials outside the conversation, prefer a low-privilege RAM credential, and rotate or delete stored keys after use.

Risk: Generated spreadsheets from untrusted invoices may contain inaccurate extracted data or unsafe spreadsheet content.

Mitigation: Review generated Excel files before relying on them for reimbursement or accounting, and handle spreadsheets from untrusted sources cautiously.

## Reference(s):

- [阿里云发票 OCR API 参考](artifact/aliyun-ocr-api.md)
- [Alibaba Cloud OCR service](https://common-buy.aliyun.com/?commodityCode=ocr_invoice_public_cn)
- [ClawHub skill page](https://clawhub.ai/1054570699/skills/invoice-recognize)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and generated XLSX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Alibaba Cloud OCR credentials and writes invoice summary spreadsheets from supported invoice documents.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
