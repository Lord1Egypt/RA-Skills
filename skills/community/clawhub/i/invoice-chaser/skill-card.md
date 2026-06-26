## Description: <br>
Invoice Chaser helps agents track unpaid invoices, configure reminder timing and templates, and support accounts receivable follow-up with escalating payment reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[audsmith28](https://clawhub.ai/user/audsmith28) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Freelancers, consultants, and small businesses use this skill to add invoices, maintain local invoice state, configure payment reminder templates, and guide follow-up workflows for overdue accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real client collection emails and escalation language. <br>
Mitigation: Use dry-run review, require human approval before firm, final, or disputed-invoice messages are sent, and customize templates for the business relationship. <br>
Risk: The reviewed bundle describes chase, status, and report scripts that are not included in the artifact. <br>
Mitigation: Do not enable cron jobs or live email sending until the missing scripts are supplied, reviewed, and tested. <br>
Risk: Invoice tracking stores client, billing, and payment-status data locally. <br>
Mitigation: Protect the local invoice data directory, validate invoice inputs, and use a dedicated billing email account for sending reminders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/audsmith28/invoice-chaser) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local invoice and configuration files under the user's invoice-chaser config directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
