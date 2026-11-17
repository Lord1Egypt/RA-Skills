## Description:

Automates overdue invoice monitoring and payment chasing for UK B2B businesses using Xero, QuickBooks, email, and WhatsApp with statutory interest calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hussainpatan9](https://clawhub.ai/user/hussainpatan9)

### License/Terms of Use:

MIT-0

## Use Case:

UK business owners, freelancers, agencies, consultants, tradespeople, and finance operators use this skill to monitor overdue Xero and QuickBooks invoices, prepare payment reminders, manage disputes, and generate aged debtor reports. It is aimed at B2B invoice collection workflows and includes UK statutory interest and fixed recovery cost language for review before use.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: The skill handles accounting, email, customer financial data, and payment history with broad permissions.

Mitigation: Use a dedicated accounting app/account and sender mailbox, verify recipient and invoice data before sends, and keep owner approval required for all outbound chases.

Risk: Credential and token handling could expose Xero, QuickBooks, email, or payment access if secrets are pasted or stored insecurely.

Mitigation: Use an encrypted credential vault when available and avoid pasting real secrets into chat or logs.

Risk: Weak retention controls can retain customer and payment history longer than intended.

Mitigation: Define retention and deletion rules for invoice, customer, chase, dispute, and payment records before enabling automation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hussainpatan9/skills/invoice-payment-chaser)
- [Xero developer apps](https://developer.xero.com/app/manage)
- [Intuit Developer apps](https://developer.intuit.com/app/developer/myapps)
- [README.md](artifact/README.md)
- [CONFIG.md](artifact/CONFIG.md)
- [EXAMPLES.md](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with invoice summaries, email drafts, reports, configuration steps, and inline command or API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include customer names, invoice amounts, due dates, payment status, dispute notes, and statutory interest calculations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
