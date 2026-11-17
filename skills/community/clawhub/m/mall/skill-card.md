## Description:

A Chinese-language shopping assistant skill that recognizes shopping intent, presents a product catalog, helps users choose items and quantities, summarizes the cart, and hands confirmed orders to a payment skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sayxxx](https://clawhub.ai/user/sayxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking users can use this skill to browse a fixed mall catalog, select products and quantities, review totals, and proceed to payment after confirmation. Developers can use it as an agent workflow for shopping-cart style product selection and checkout handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order totals or quantities may be wrong before checkout.

Mitigation: Review the item quantities, subtotals, and final total carefully before confirming payment.

Risk: The skill hands confirmed orders to a separate payment skill.

Mitigation: Use it only with a payment skill you trust, and rely on that payment skill to create payment details.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style conversational text with product lists, cart summaries, totals, and payment handoff status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires accurate quantity and total calculations before payment confirmation; payment details are returned by a separate payment skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
