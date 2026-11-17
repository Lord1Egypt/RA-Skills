## Description:

Create and send professional invoices with automatic numbering, tax calculation, templates, and payment tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Freelancers and small business operators use this skill to prepare client invoices, calculate taxes, generate invoice PDFs, optionally send them, and track payment status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive billing records including tax IDs, addresses, email addresses, invoice PDFs, and payment details.

Mitigation: Keep billing data in the intended local billing directory and install only when comfortable storing those records there.

Risk: Incorrect client details, invoice numbers, totals, or recipients can create billing, tax, or delivery errors.

Mitigation: Review client records, invoice numbers, totals, taxes, due dates, and email recipients before finalizing or sending invoices.

Risk: Finalized invoice numbers may be difficult to correct by simple deletion.

Mitigation: Use credit notes or correction workflows when an already finalized invoice needs correction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/invoice)
- [Invoice Creation Phases](artifact/phases.md)
- [Client Database](artifact/clients.md)
- [Invoice Legal Requirements](artifact/legal.md)
- [Invoice Templates](artifact/templates.md)
- [Invoice Types](artifact/types.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown, JSON records, invoice PDFs, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft invoice files, finalized PDF invoices, client records, series counters, configuration guidance, and optional email-ready invoice content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
