## Description:

Use to authenticate with Morning (GreenInvoice) and create/manage clients, items, and accounting documents (invoice/receipt/quote/order/credit).

This skill is ready for commercial/non-commercial use.

## Publisher:

[k0renn](https://clawhub.ai/user/k0renn)

### License/Terms of Use:


## Use Case:

External users and business operators use this skill to have an agent authenticate with Morning/GreenInvoice, maintain client and item records, and create invoices, receipts, quotes, orders, credit invoices, or debit invoices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify Morning/GreenInvoice business records when given valid API credentials.

Mitigation: Provide client, document, currency, and language details explicitly for important accounting actions and review them before execution.

Risk: API secrets and JWTs are sensitive credentials.

Mitigation: Do not log, echo, or include API secrets or JWTs in user-facing responses.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Configuration]

**Output Format:** [Markdown guidance with JSON tool payload examples and concise text outputs such as resource IDs and document URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or relay created client, item, and document identifiers, plus document links when the Morning/GreenInvoice tool provides them.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
