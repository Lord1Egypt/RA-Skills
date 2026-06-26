## Description: <br>
上传发票图片或文件进行 OCR 识别，并返回发票票面结构化信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxt](https://clawhub.ai/user/zxt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business operations teams use this skill to extract invoice numbers, dates, amounts, buyer and seller details, tax information, and line items from PDF, OFD, JPEG, JPG, PNG, or XML invoice files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if pasted into chat or stored persistently in shell startup files or user-level environment settings. <br>
Mitigation: Set ZXT_API_KEY directly in a trusted local environment or secret manager, use short-lived or revocable credentials where possible, and avoid writing secrets to persistent shell configuration unless that exposure is acceptable. <br>
Risk: Invoice files and extracted invoice data are sent to a third-party OCR service. <br>
Mitigation: Use the skill only for invoices the user is authorized to submit to the listed service, and avoid sending sensitive documents unless the service terms and data-handling requirements are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zxt/invoice-ocr-pro) <br>
- [Publisher profile](https://clawhub.ai/user/zxt) <br>
- [API key registration service](https://skill.quandianfapiao.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown or plain text with OCR result fields and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns structured invoice fields such as invoice number, date, amounts, buyer and seller details, tax values, remarks, and line items.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
