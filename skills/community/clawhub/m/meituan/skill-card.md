## Description:

Meituan public local-life decision assistant that compares visible merchant, fee, discount, ETA, review-risk, threshold, and refund-friction signals, then recommends whether to order, switch, add a useful item, wait, or skip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to decide whether a Meituan food delivery or local-life offer is worth acting on from public pages, screenshots, or copied cart details. It helps compare real payable tradeoffs, delivery timing, merchant trust, threshold discounts, and manual pre-order checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Final price, ETA, stock, coupon eligibility, refund terms, and payment state may depend on account or checkout state that the skill does not access.

Mitigation: Verify final payable amount, address-based ETA, account coupon eligibility, item options, stock, refund or after-sales rule, delivery note, and payment details in Meituan before ordering.

Risk: Screenshots or copied order details may contain personal data.

Mitigation: Redact phone numbers, addresses, names, order IDs, and payment details before sharing screenshots or copied text with an agent.

Risk: Authenticated account actions, cart changes, checkout, or payment could create unwanted platform or purchase effects.

Mitigation: Keep use to visible public evidence and user-provided details; stop at login, CAPTCHA, address selection, coupon wallet, order, checkout, or payment screens.

## Reference(s):

- [ClawHub Meituan Skill Page](https://clawhub.ai/harrylabsj/skills/meituan)
- [ClawHub Publisher Profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [guidance, analysis, markdown]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a concise decision, checkout-reality analysis, risk check, confidence level, evidence gaps, and user-only checks before ordering.]

## Skill Version(s):

2.2.0 (source: frontmatter, package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
