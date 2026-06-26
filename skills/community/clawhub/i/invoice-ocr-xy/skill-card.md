## Description: <br>
发票 OCR 识别技能，可扫描文件夹中的发票文件（PDF/图片），调用翔云 OCR API 识别发票信息，并支持 40+ 种发票类型。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liudengkui](https://clawhub.ai/user/liudengkui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to batch process invoice PDFs, OFD files, and images through NetOCR and extract structured invoice details for review or export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice files may contain sensitive financial, tax, or personal data and are sent to the NetOCR service for recognition. <br>
Mitigation: Use the skill only with invoices approved for third-party OCR processing and review applicable data-handling requirements before use. <br>
Risk: NetOCR API credentials are required and may be stored in the skill configuration file. <br>
Mitigation: Configure credentials locally with the --config command, use quota-controlled keys, and protect or remove config.json after use. <br>
Risk: Excel export may trigger dependency installation for openpyxl if it is missing. <br>
Mitigation: Preinstall openpyxl through normal package-management controls before running exports. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liudengkui/invoice-ocr-xy) <br>
- [NetOCR](https://netocr.com) <br>
- [NetOCR Invoice OCR API Reference](https://www.netocr.com/invoiceFor2.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Console text with optional JSON or XLSX export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided NetOCR credentials and sends invoice content to the NetOCR service.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
