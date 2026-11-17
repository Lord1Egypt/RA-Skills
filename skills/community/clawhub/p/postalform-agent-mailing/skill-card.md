## Description:

Guides an agent through preparing, validating, paying for, and polling a PostalForm machine order to send a real physical document by mail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggaabe](https://clawhub.ai/user/ggaabe)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when an agent needs to send a PDF as real postal mail through PostalForm with validation, payment settlement, and fulfillment polling.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can transmit letter contents, names, email, and postal addresses to PostalForm.

Mitigation: Review document contents and sender, recipient, and buyer details before validation, payment, or submission.

Risk: The workflow can spend wallet funds and trigger irreversible physical delivery.

Mitigation: Require final human approval before payment, use a strict payment cap, and verify quote price and page count before submitting the paid order.

Risk: Wallet secrets or full payloads may be exposed through logs or process arguments.

Mitigation: Use encrypted keystores or wallet aliases, read passwords from secure runtime input, and avoid logging credentials, sensitive environment variables, or full document payloads.

## Reference(s):

- [Payload Templates](references/payload_templates.md)
- [PostalForm machine order validation endpoint](https://postalform.com/api/machine/orders/validate)
- [PostalForm machine order endpoint](https://postalform.com/api/machine/orders)
- [PostalForm machine order status endpoint](https://postalform.com/api/machine/orders/:request_id)

## Skill Output:

**Output Type(s):** [guidance, json, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON payload templates and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns order identifiers, quote summary, payment settlement details, latest fulfillment status, and completion URL when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
