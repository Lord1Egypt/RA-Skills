## Description: <br>
Create and send professional invoices with automatic numbering, tax calculation, templates, and payment tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Freelancers and small businesses use this skill to draft, review, finalize, optionally send, and track outgoing invoices while keeping client data, numbering, tax calculation, templates, and payment status organized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive billing information, including client billing data, tax IDs, invoice PDFs, and payment details. <br>
Mitigation: Keep billing records protected, limit access to ~/billing, and delete old records when they are no longer needed. <br>
Risk: Incorrect invoice numbers, amounts, tax treatment, client data, or email recipients could create business or compliance problems. <br>
Mitigation: Review invoice numbers, totals, tax handling, stored client data, and recipients before finalizing or sending invoices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/invoice) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Invoice creation phases](artifact/phases.md) <br>
- [Client database guidance](artifact/clients.md) <br>
- [Invoice templates](artifact/templates.md) <br>
- [Invoice types](artifact/types.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with invoice drafts, client records, configuration examples, template code, and optional shell commands for PDF generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local billing files, invoice PDFs, client records, numbering state, and payment status notes under ~/billing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
