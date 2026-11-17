## Description:

Order food and drinks on a paired Android device using an in-app menu and cart, with commands to view goods, add or remove items, clear the cart, and submit a demo order with no real payment.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[04551lh](https://clawhub.ai/user/04551lh)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to manage a demo food or drink cart on a paired Android device, including viewing the menu, adding or removing items, checking the cart, and submitting the current demo order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate a demo cart and submit the current cart in the paired Android app.

Mitigation: Review the cart contents and total with the user before allowing order.submitOrder.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/04551lh/skills/order)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Configuration]

**Output Format:** [Markdown guidance with JSON command parameters and command names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OpenClaw order commands against a paired Android device; order submission is demo-only and does not process payment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
