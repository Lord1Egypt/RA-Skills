## Description:

Helps agents pay invoices through the Mercury Bank API, manage recipients, query transactions, perform authorized transfers, and notify bookkeeping and vendors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nathan-deepmm](https://clawhub.ai/user/nathan-deepmm)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to prepare and execute approved Mercury ACH, wire, recipient-management, transfer, and transaction-query workflows for invoice payment operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact money movement could send payments or transfers incorrectly if executed without proper authorization.

Mitigation: Require explicit approval from an authorized operator for every payment or transfer, including amount, recipient, invoice number, and account.

Risk: Broad Mercury credentials could expose financial accounts beyond the intended workflow.

Mitigation: Use only narrowly scoped Mercury credentials and confirm the default payment account at payment time.

Risk: Invoice contents and payment details could be exposed through memory, logs, or email attachments.

Mitigation: Do not store invoice contents or full payment details in general agent memory, and attach invoice PDFs only for recipients authorized to receive them.

Risk: Internal transfers post instantly and may bypass separate business controls.

Mitigation: Avoid internal transfers unless separately authorized for the specific source account, destination account, amount, and idempotency key.

## Reference(s):

- [Mercury Payments Skill Page](https://clawhub.ai/nathan-deepmm/skills/mercury-payments)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and payment workflow checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires human approval before money movement and narrowly scoped Mercury credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
