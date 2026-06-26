## Description: <br>
Automates overdue UK B2B invoice chasing through Xero and QuickBooks with email and WhatsApp reminders, statutory interest calculations, dispute handling, payment detection, and aged debtor reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hussainpatan9](https://clawhub.ai/user/hussainpatan9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
UK businesses that invoice clients, including freelancers, agencies, consultants, tradespeople, and service businesses, use this skill to monitor overdue invoices, prepare or send staged payment chases, manage disputes, and report on aged debtors. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires powerful accounting, email, and OAuth credentials. <br>
Mitigation: Use dedicated least-privilege accounts or a credential vault, avoid pasting long-lived secrets into chat, and keep tokens hidden from transcripts and logs. <br>
Risk: The skill can send sensitive payment-chasing messages to customers. <br>
Mitigation: Keep approval required for outbound messages, especially final demands, and verify each recipient, invoice, amount, and due date before sending. <br>
Risk: Invoice and customer data may be transmitted through email and WhatsApp. <br>
Mitigation: Confirm the business is allowed to process and transmit customer invoice data through the configured channels before deployment. <br>
Risk: Statutory interest and debt recovery language applies only to eligible UK B2B debts and is not legal advice. <br>
Mitigation: Verify B2B eligibility, confirm the current Bank of England base rate before Stage 3 or Stage 4 notices, and seek legal advice before court or debt collection escalation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hussainpatan9/invoice-payment-chaser) <br>
- [Publisher profile](https://clawhub.ai/user/hussainpatan9) <br>
- [Xero developer apps](https://developer.xero.com/app/manage) <br>
- [Intuit QuickBooks developer apps](https://developer.intuit.com/app/developer/myapps) <br>
- [artifact/README.md](artifact/README.md) <br>
- [artifact/CONFIG.md](artifact/CONFIG.md) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with code blocks, API request examples, configuration values, invoice summaries, chase email drafts, and reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare or send customer-facing email and WhatsApp payment chases after configured approvals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
