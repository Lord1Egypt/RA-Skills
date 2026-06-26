## Description: <br>
Generates, manages, and downloads professional PDF invoices through the InvoiceForge API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jbennett111](https://clawhub.ai/user/Jbennett111) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Freelancers, agencies, consultants, small businesses, SaaS teams, and contractors use this skill to create invoices, download invoice PDFs, track invoice status, and automate billing workflows through InvoiceForge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice workflows can send seller, buyer, email, address, line-item, tax, due-date, and note data to the third-party InvoiceForge service. <br>
Mitigation: Confirm the invoice payload and obtain user consent before each invoice creation, batch operation, or status update. <br>
Risk: InvoiceForge API keys grant access to invoice operations and could expose billing workflows if stored insecurely. <br>
Mitigation: Store the API key only in a trusted secret manager and avoid placing it in chat history, source files, or shell history. <br>


## Reference(s): <br>
- [InvoiceForge API](https://invoiceforge.vosscg.com) <br>
- [InvoiceForge API key endpoint](https://invoiceforge.vosscg.com/v1/keys) <br>
- [InvoiceForge invoices endpoint](https://invoiceforge.vosscg.com/v1/invoices) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce invoice API requests, invoice status updates, PDF download commands, and API-key setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
