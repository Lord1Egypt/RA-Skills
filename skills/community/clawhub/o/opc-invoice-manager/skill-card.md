## Description: <br>
Accounts Receivable light system for solo entrepreneurs that supports invoice generation, collections follow-up, payment reconciliation, aging analysis, and cash flow visibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeonFJR](https://clawhub.ai/user/LeonFJR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Solo entrepreneurs and one-person company operators use this skill to create invoices, track receivables, draft collection follow-ups, reconcile payments, and review AR dashboards from local invoice records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated invoices, void or reissue actions, payment status changes, and client-profile updates may become business records if accepted without review. <br>
Mitigation: Use the skill in a dedicated invoice folder, keep backups, and review generated invoices, archive changes, payment updates, and collection emails before sending or treating them as records. <br>
Risk: Tax-related invoice questions can require jurisdiction-specific professional judgment. <br>
Mitigation: Do not treat the skill as tax advice; confirm tax rates, compliance rules, credit notes, write-offs, and cross-border tax issues with a qualified accountant. <br>
Risk: Local invoice indexing and tracking scripts read and write billing files that may contain sensitive client, payment, and receivables data. <br>
Mitigation: Run the scripts only against the intended invoice directory, restrict access to that folder, and review generated indexes and reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LeonFJR/opc-invoice-manager) <br>
- [Invoice Best Practices](references/invoice-best-practices.md) <br>
- [Collections Playbook](references/collections-playbook.md) <br>
- [Payment Terms Guide](references/payment-terms-guide.md) <br>
- [Tax & Compliance Awareness](references/tax-and-compliance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown invoices and reports, JSON metadata, HTML invoice templates, and shell commands for local invoice utilities] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses exact decimal-safe monetary strings and ISO 8601 dates for generated invoice metadata.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
