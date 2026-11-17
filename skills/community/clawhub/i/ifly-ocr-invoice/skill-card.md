## Description:

Recognize and extract structured data from invoices, receipts, and bills using the iFlytek OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingzhe2020](https://clawhub.ai/user/qingzhe2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use this skill to send invoice, receipt, and bill images to iFlytek OCR and receive structured extracted fields for expense, finance, and document processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice, receipt, medical, bank, tax, or other sensitive financial images may be sent to iFlytek's OCR service.

Mitigation: Use the skill only when sharing those documents with the third-party OCR service is acceptable under the user's privacy, contractual, and compliance requirements.

Risk: Troubleshooting commands in the artifact can print XFYUN_API_KEY or XFYUN_API_SECRET into logs, screenshots, or support chats.

Mitigation: Use presence-only or masked credential checks, and rotate iFlytek credentials if secrets were exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingzhe2020/skills/ifly-ocr-invoice)
- [iFlytek Console](https://console.xfyun.cn)
- [iFlytek Invoice Recognition Service](https://www.xfyun.cn/services/Invoice_recognition?target=price)
- [iFlytek Invoice Recognition API endpoint](https://api.xf-yun.com/v1/private/sc45f0684)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Human-readable text or raw JSON from the command-line OCR script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XFYUN_APP_ID, XFYUN_API_KEY, and XFYUN_API_SECRET environment variables; processes local image or PDF paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
