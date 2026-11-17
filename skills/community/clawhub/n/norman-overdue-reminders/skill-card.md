## Description:

Find overdue invoices and send payment reminders (Zahlungserinnerungen / Mahnungen) to clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanlee000](https://clawhub.ai/user/stanlee000)

### License/Terms of Use:


## Use Case:

Business users and finance operators use this skill to identify unpaid invoices, group overdue accounts by reminder severity, review client contact details, and approve payment reminders before they are sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses invoice, client contact, and transaction data through the norman-finance MCP connection.

Mitigation: Install and use it only where that connection is trusted for financial and client-contact data.

Risk: Formal Mahnung or final-notice reminders can affect legal position and customer relationships.

Mitigation: Review each reminder carefully and require explicit user approval before any reminder is sent.

Risk: An invoice may appear overdue when a recent payment has not yet been linked.

Mitigation: Check recent transactions before sending reminders for invoices that may have already been paid.

## Reference(s):

- [Norman Finance](https://norman.finance)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown summaries, invoice tables, approval prompts, and final reminder reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user review and explicit approval before sending each reminder.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
