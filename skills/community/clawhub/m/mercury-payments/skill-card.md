## Description: <br>
Assists with Mercury Bank payment workflows, including approved invoice payments, recipient setup, internal transfers, transaction queries, and invoice-backed notification emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nathan-deepmm](https://clawhub.ai/user/nathan-deepmm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Authorized operators and finance-supporting agents use this skill to prepare and execute approved Mercury payments, manage payment recipients and transfers, query transactions, and send invoice-backed payment confirmations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through real Mercury banking actions with write-level payment authority. <br>
Mitigation: Use the narrowest Mercury token available, require explicit approval from an authorized operator, and independently verify every recipient, amount, account, invoice, and email thread before execution. <br>
Risk: Mercury tokens, bank details, invoices, and payment records may expose sensitive financial information. <br>
Mitigation: Avoid storing tokens or bank details in memory logs, keep invoice PDFs only as long as needed, and delete downloaded invoice files after use. <br>
Risk: Incorrect or duplicate payment requests can move money to the wrong recipient or repeat a transaction. <br>
Mitigation: Confirm the selected account and recipient at payment time, use descriptive idempotency keys, and review the payment response before sending bookkeeping or vendor confirmations. <br>


## Reference(s): <br>
- [Mercury Payments on ClawHub](https://clawhub.ai/nathan-deepmm/mercury-payments) <br>
- [Mercury API](https://api.mercury.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Mercury API curl commands, recipient and payment payload examples, operational checklists, and email draft guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
