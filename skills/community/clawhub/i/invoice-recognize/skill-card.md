## Description: <br>
发票识别 scans invoice PDFs, OFD files, and images, sends them to Alibaba Cloud OCR for field extraction, and exports the results to an Excel workbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1054570699](https://clawhub.ai/user/1054570699) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to batch-process invoice folders for reimbursement or bookkeeping workflows, extracting common invoice fields into an xlsx summary file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice files are sent to Alibaba Cloud OCR for processing. <br>
Mitigation: Use the skill only for invoices that may be shared with Alibaba Cloud, and point it at a narrow invoice-only folder. <br>
Risk: Alibaba Cloud AccessKey credentials may be exposed if pasted into chat or left unprotected in config.json. <br>
Mitigation: Configure credentials locally, use a dedicated least-privilege RAM AccessKey, avoid sharing secrets in chat, and protect or delete config.json after use. <br>
Risk: OCR usage may incur Alibaba Cloud charges. <br>
Mitigation: Monitor Alibaba Cloud OCR usage and set billing alerts or quotas before batch processing large folders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1054570699/invoice-recognize) <br>
- [Aliyun OCR API reference](aliyun-ocr-api.md) <br>
- [Alibaba Cloud invoice OCR service](https://common-buy.aliyun.com/?commodityCode=ocr_invoice_public_cn) <br>
- [Alibaba Cloud](https://www.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is an Excel xlsx file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script reads a folder of invoices and can save credentials in config.json before exporting 发票汇总.xlsx or a user-specified xlsx path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
