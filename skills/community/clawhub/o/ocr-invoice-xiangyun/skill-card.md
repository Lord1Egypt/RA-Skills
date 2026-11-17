## Description:

Recognizes, verifies, batch-processes, and optionally exports Chinese invoice data using Xiangyun/NetOCR APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liudengkui](https://clawhub.ai/user/liudengkui)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, accounting, tax, and operations users can use this skill through an agent to OCR Chinese invoice files, verify supported invoice types, process folders in batch, and create invoice workbooks when export is explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice contents and NetOCR API credentials are sent to netocr.com for OCR and verification.

Mitigation: Install and use the skill only when that third-party processing is acceptable for the invoice data involved.

Risk: Local config.json or generated result files may expose credentials or invoice data if shared or committed.

Mitigation: Keep the skill directory private, do not commit config.json or generated JSON/XLSX files, and rotate credentials if exposure is suspected.

Risk: Exported spreadsheets may contain untrusted invoice field values.

Mitigation: Treat generated workbooks as untrusted and sanitize formula-like fields before sharing or opening them in sensitive environments.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liudengkui/skills/ocr-invoice-xiangyun)
- [NetOCR service](https://netocr.com)
- [NetOCR invoice OCR API](https://netocr.com/api/v2/recogInvoiveBase64.do)
- [NetOCR invoice verification API](https://netocr.com/verapi/v2/verInvoice.do)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with CLI commands; JSON API results and optional XLSX exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NetOCR key/secret; sends selected invoice files to netocr.com; export runs only when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
