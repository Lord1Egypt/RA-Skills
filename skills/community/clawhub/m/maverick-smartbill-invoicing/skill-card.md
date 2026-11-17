## Description:

Issue SmartBill invoices through the SmartBill.ro API with local automation for validating invoice payloads, creating invoices, listing document series, and downloading invoice PDFs by series and number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, finance operators, and automation agents use this skill to validate SmartBill invoice payloads, create draft or final invoices after confirmation, list document series, and retrieve invoice PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable SmartBill API URL can redirect SmartBill credentials and invoice data to an unapproved server.

Mitigation: Use the default SmartBill API host and do not set MAVERICK_SMARTBILL_API_BASE or --base-url from untrusted input.

Risk: Final invoice creation can have business and customer-data impact.

Mitigation: Run a dry-run first and require explicit human confirmation before using --allow-final.

Risk: Debug logging can expose real customer or invoice data.

Mitigation: Keep debug mode disabled around production data and real customer records.

## Reference(s):

- [SmartBill API Notes](references/smartbill-api.md)
- [Invoice Example](references/invoice-example.json)
- [SmartBill API Base URL](https://ws.smartbill.ro/SBORO/api)
- [ClawHub Skill Page](https://clawhub.ai/maverick/skills/maverick-smartbill-invoicing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local JSON validation or API responses and invoice PDF files when the CLI is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
