## Description:

Use the user's signed-in Harris Teeter browser session to find grocery products and prices, manage a cart, check pickup windows, and view order history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to find Harris Teeter products and prices, update or review a grocery cart, check pickup options, and look up past orders. A separate, short-lived pharmacy sign-in also enables prescription lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prescription lookups can expose sensitive records, including information for linked patient profiles; the security scan was incomplete.

Mitigation: Review this capability before installation. Use pharmacy lookup only when needed, keep returned patient information private, and note that pharmacy access requires a separate, short-lived sign-in.

Risk: Cart and coupon commands can change the user's shopping state, and an unavailable product may not be added as expected.

Mitigation: Resolve products by search, re-read the cart after changes, and place any order through the Harris Teeter website where the user confirms it.

## Reference(s):

- [Harris Teeter request reference](references/requests.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON results with shell command examples and concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive results depend on the user's signed-in browser session; order placement is completed by the user on the Harris Teeter website.]

## Skill Version(s):

0.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
