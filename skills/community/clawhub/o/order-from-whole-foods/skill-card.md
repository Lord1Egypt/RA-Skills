## Description:

Order groceries from Whole Foods using browser automation and a saved purchase policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chadnewbry](https://clawhub.ai/user/chadnewbry)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn a grocery list into a Whole Foods online cart or order while following their saved purchase, delivery-window, and calendar preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place Whole Foods orders automatically when saved policy allows, which may create charges without a per-order review.

Mitigation: Use add_to_cart_only or confirm_before_buy:true for final approval, and set max_auto_spend conservatively.

Risk: Confirmed delivery or pickup windows may be written to the user's calendar when calendar blocking is enabled.

Mitigation: Disable calendar_blocking_enabled if delivery details should not be added to the calendar.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chadnewbry/skills/order-from-whole-foods)
- [Whole Foods Amazon storefront](https://www.amazon.com/alm/storefront?almBrandId=VUZHIFdob2xlIEZvb2Rz&ref=nav_cs_dsk_grfl_stfr_wf)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Browser actions, Markdown]

**Output Format:** [Concise Markdown status summary with setup questions, cart or order details, and blocker recovery steps when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report order placed, cart ready for review, or blocked; does not invent prices, delivery windows, or cart state.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
