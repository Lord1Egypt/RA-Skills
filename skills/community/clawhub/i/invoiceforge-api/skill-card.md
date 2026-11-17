## Description:

Generate professional PDF invoices using InvoiceForge API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbennett111](https://clawhub.ai/user/jbennett111)

### License/Terms of Use:


## Use Case:

Developers, freelancers, agencies, consultants, contractors, SaaS companies, and small businesses use this skill to create, list, download, and update invoices through InvoiceForge after collecting billing details and confirming API actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice creation and management sends seller, buyer, invoice, email, and payment-status information to the third-party InvoiceForge service.

Mitigation: Confirm the intended account, invoice contents, recipients, and status changes before allowing the agent to call the API.

Risk: The skill requires an InvoiceForge API key that could expose billing operations if stored or shared improperly.

Mitigation: Store the API key only in an approved secret store and avoid placing it in chat logs, source files, or generated documents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jbennett111/skills/invoiceforge-api)
- [InvoiceForge API Base URL](https://invoiceforge.vosscg.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, files]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide API key storage and produce invoice PDF downloads when the generated API calls are executed.]

## Skill Version(s):

1.0.0 (source: package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
