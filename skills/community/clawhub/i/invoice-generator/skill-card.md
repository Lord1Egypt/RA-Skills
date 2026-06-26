## Description: <br>
Generate professional PDF invoices from JSON data for invoices, billing documents, or payment requests with company, client, and line-item details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmigone](https://clawhub.ai/user/tmigone) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to generate local PDF invoices from structured JSON supplied by stdin, a file path, or a saved invoice config. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated invoices may contain private billing, tax, company, or client information written to local disk. <br>
Mitigation: Set INVOICE_DIR to a dedicated private folder and avoid shared or synced locations unless that sharing is intended. <br>
Risk: The artifact references an invoice template at assets/invoice.hbs that was not included in the reviewed files. <br>
Mitigation: Confirm the template is present and review it before relying on generated invoice PDFs. <br>


## Reference(s): <br>
- [Invoice Data Schema](references/data-schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/tmigone/invoice-generator) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [PDF file path on stdout, with errors on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local PDF files under INVOICE_DIR/invoices and auto-versions duplicate invoice filenames.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
