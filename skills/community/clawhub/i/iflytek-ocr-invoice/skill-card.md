## Description:

Recognizes invoices, receipts, bills, and tickets by sending supported image or PDF files to the iFlytek OCR API and returning extracted structured fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflytek.skills](https://clawhub.ai/user/iflytek.skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and business users use this skill to extract structured invoice, receipt, ticket, and bill data for expense reporting, archiving, or downstream document processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoices, receipts, bank slips, or medical bills may contain sensitive data that is uploaded to iFlytek's cloud OCR service.

Mitigation: Run the skill only when authorized to send the target documents to iFlytek, and avoid processing documents whose privacy, contractual, or regulatory constraints forbid third-party cloud OCR.

Risk: The documentation includes environment-check commands that can print full API credentials.

Mitigation: Use masked or presence-only checks, store credentials in a protected secret manager or restricted environment file, and rotate the API key and secret if they were exposed in logs, screenshots, or chat.

## Reference(s):

- [iFlytek OCR Service](https://www.xfyun.cn/services/ocr)
- [iFlytek Invoice Recognition](https://www.xfyun.cn/services/Invoice_recognition)
- [iFlytek Console](https://console.xfyun.cn)
- [ClawHub Skill Page](https://clawhub.ai/iflytek.skills/skills/iflytek-ocr-invoice)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Human-readable structured text by default, or raw JSON when invoked with --raw]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and XFYUN_APP_ID, XFYUN_API_KEY, and XFYUN_API_SECRET environment variables.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
