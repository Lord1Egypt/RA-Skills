## Description:

Unified food ordering assistant for India that supports Swiggy and Zomato workflows with strict pre-order confirmation, cart preview, address checks, and vendor fallback logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anugotta](https://clawhub.ai/user/anugotta)

### License/Terms of Use:

MIT-0

## Use Case:

External users in India use this skill to compare food-ordering options across supported vendors, assemble a cart, confirm delivery details, and place an order only after explicit approval.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: The skill may guide an agent through real food purchases using vendor connectors and delivery address information.

Mitigation: Use only trusted connectors and require the user to review the vendor, cart, total, ETA, address, and cancellation or payment terms before confirming.

Risk: Vendor availability, pricing, ETA, cancellation rights, and payment behavior can change before checkout.

Mitigation: Refresh vendor data during cart review and surface COD-only or non-cancellable constraints before asking for final confirmation.

Risk: Ambiguous saved address labels or checkout retries can lead to wrong delivery details or duplicate orders.

Mitigation: Confirm the exact delivery address and avoid automatic order-placement retries after payment or checkout failures.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anugotta/skills/india-food-ordering)
- [ClawHub Homepage Metadata](https://clawhub.ai/regalstreak/swiggy)
- [Setup](setup.md)
- [Vendor Playbook](vendor-playbook.md)
- [Examples](examples.md)
- [Validation Checklist](validation-checklist.md)
- [Launch Playbook](launch-playbook.md)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, configuration]

**Output Format:** [Markdown response with ordering options, vendor recommendation, cart summary, and confirmation prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before order placement and returns an order reference after confirmed checkout when a trusted connector supports it.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
