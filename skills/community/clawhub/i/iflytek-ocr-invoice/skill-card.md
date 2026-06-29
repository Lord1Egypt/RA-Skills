## Description: <br>
Recognizes invoices, receipts, bills, tickets, and similar documents by sending images or PDFs to the iFlytek OCR API and returning extracted structured fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflytek.skills](https://clawhub.ai/user/iflytek.skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to digitize invoice, receipt, bill, ticket, and medical document images into structured OCR output for tasks such as expense reporting, archiving, and data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice, receipt, bill, medical, and travel document images may contain sensitive information and are sent to a third-party OCR API. <br>
Mitigation: Install and use this skill only when sending those documents to iFlytek is acceptable for the user's privacy, security, and compliance requirements. <br>
Risk: The artifact includes troubleshooting commands that can print full XFYUN credentials into terminal output or logs. <br>
Mitigation: Check only whether credential variables are set, mask values in logs, and rotate XFYUN credentials if they were exposed. <br>


## Reference(s): <br>
- [iFlytek OCR service](https://www.xfyun.cn/services/ocr) <br>
- [iFlytek invoice recognition documentation](https://www.xfyun.cn/services/Invoice_recognition) <br>
- [iFlytek invoice recognition pricing](https://www.xfyun.cn/services/Invoice_recognition?target=price) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable structured text by default, or raw JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and XFYUN_APP_ID, XFYUN_API_KEY, and XFYUN_API_SECRET; submitted document files are sent to the iFlytek OCR API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
