## Description: <br>
Recognize and extract structured data from invoices, receipts, and bills using iFlytek OCR API (科大讯飞票据识别). Supports VAT invoices, taxi receipts, train tickets, toll invoices, medical bills, bank receipts, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingzhe2020](https://clawhub.ai/user/qingzhe2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and expense operations teams use this skill to submit invoice, receipt, and bill images or PDFs to iFlytek OCR and receive structured invoice data for digitization or expense workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The troubleshooting guide includes commands that print XFYUN_API_KEY and XFYUN_API_SECRET in full. <br>
Mitigation: Do not run commands that echo secrets; verify environment variables with redacted checks and rotate any credentials that were printed or shared. <br>
Risk: Invoice and receipt files are sent to the iFlytek OCR API for processing. <br>
Mitigation: Use only documents you are authorized to send to iFlytek and confirm the service terms, data handling requirements, and regional compliance obligations before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingzhe2020/ifly-ocr-invoice) <br>
- [iFlytek Console](https://console.xfyun.cn) <br>
- [iFlytek invoice recognition service](https://www.xfyun.cn/services/Invoice_recognition?target=price) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable text or raw JSON from a command-line Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XFYUN_APP_ID, XFYUN_API_KEY, and XFYUN_API_SECRET environment variables and sends provided document files to the iFlytek OCR API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
