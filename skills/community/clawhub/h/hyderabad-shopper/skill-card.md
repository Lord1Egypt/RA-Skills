## Description:

Finds lowest prices for pincode 500081 in Hyderabad while limiting platform searches to reduce browser memory usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sparshkhandelwal28](https://clawhub.ai/user/sparshkhandelwal28)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this shopping assistant to compare grocery and commerce prices for Hyderabad pincode 500081 and receive a Markdown summary before choosing whether to proceed to checkout. If asked to buy, the skill prepares the cart but requires the user to complete payment manually.

### Deployment Geography for Use:

Hyderabad, India (pincode 500081)

## Known Risks and Mitigations:

Risk: The skill can prepare carts and send checkout screenshots through Telegram, which may expose order, account, or delivery details outside the shopping site.

Mitigation: Install only if external Telegram handoff is expected, require explicit approval before sending screenshots, and review checkout content before sharing.

Risk: The package contains a hardcoded full delivery address in metadata.

Mitigation: Remove the full address from the package or replace it with user-provided runtime location data before distribution.

Risk: Checkout automation may add items and navigate to the final payment screen.

Mitigation: Keep the documented human-in-the-loop pause and do not allow the agent to click payment or order confirmation controls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sparshkhandelwal28/skills/hyderabad-shopper)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown table with checkout handoff text when purchase flow is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches priority platforms one at a time, reports timeouts, and pauses before payment confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
