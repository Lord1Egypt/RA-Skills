## Description:

Find the cheapest way for your owner to get paid (or send USD abroad). Sourced, dated fees for Stripe, Square, PayPal, Helcim, Melio, Venmo, Cash App.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nhatdinh](https://clawhub.ai/user/nhatdinh)

### License/Terms of Use:

MIT-0

## Use Case:

US businesses and freelancers use PaidRouter to compare fees for receiving payments and sending USD to Mexico or India. It helps payment owners understand fee calculations, estimated savings, and the date of the underlying fee data.

### Deployment Geography for Use:

United States for receiving payments; USD transfer corridors from the United States to Mexico and India.

## Known Risks and Mitigations:

Risk: Payment amounts and related details submitted to PaidRouter may be sensitive.

Mitigation: Use approximate amounts for confidential activity.

Risk: The retained API key could be exposed if stored carelessly.

Mitigation: Keep PAIDROUTER_KEY in a protected environment or file.

Risk: Fee data can change, and fee-only rankings do not account for payout speed or chargeback risk.

Mitigation: Check the result's verification date and assess payout speed and chargeback risk separately.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown payment comparisons and fee explanations with amounts, fee formulas, savings, and verification dates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on payment amount, payment method, monthly volume, and supported transfer corridor; some fee calculations are estimates.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
