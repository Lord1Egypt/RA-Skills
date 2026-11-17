## Description:

Accounts Receivable light system for solo entrepreneurs that manages invoice generation, collections follow-up, payment reconciliation, aging analysis, and cash flow visibility with optional contract data integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonfjr](https://clawhub.ai/user/leonfjr)

### License/Terms of Use:

MIT-0

## Use Case:

Solo entrepreneurs and one-person company CEOs use this skill to create invoices, draft collection follow-ups, reconcile payments, manage client receivables profiles, and review aging and revenue summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change invoice metadata, payment status, outstanding balances, and local invoice indexes.

Mitigation: Review generated file changes and payment updates before relying on them, and keep the invoice archive protected and backed up.

Risk: Customer-facing invoices and collection drafts may contain incorrect, misleading, or unescaped contract or client-profile content.

Mitigation: Review every invoice and collection draft before sending, and avoid untrusted contract or client-profile text until HTML and Markdown escaping is confirmed.

Risk: Payment updates may be unreliable if amounts are not positive or dates are not real.

Mitigation: Validate payment amounts and dates against source records before marking invoices paid or partially paid.

Risk: Tax and compliance topics can exceed the skill's invoicing scope.

Mitigation: Use accountant review for tax decisions, cross-border invoicing, credit notes with tax implications, and jurisdiction-specific compliance questions.

## Reference(s):

- [Invoice Best Practices](references/invoice-best-practices.md)
- [Tax & Compliance Awareness](references/tax-and-compliance.md)
- [Payment Terms Guide](references/payment-terms-guide.md)
- [Collections Playbook](references/collections-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Configuration]

**Output Format:** [Markdown invoices and reports, JSON invoice and client metadata, optional HTML invoices, shell commands, configuration files, and ready-to-send email draft text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local invoice archive files, client profiles, invoice indexes, payment status fields, and analytics summaries.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
