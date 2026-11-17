## Description:

Pinduoduo shopping assistant. Input a product name or PDD link; evaluate 百亿补贴, 拼团 rules, seller risk, visible price, review signals, refund caveats, and whether the low price is worth it. Safe boundary: no login, no order submission, no payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT

## Use Case:

External shoppers and shopping agents use this skill to evaluate Pinduoduo products, group-buy and subsidy mechanics, seller trust, review signals, and refund caveats before deciding whether a low price is worth the risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged-in PDD workflows can change cart, coupon, and group-buy state and may expose checkout-preview details.

Mitigation: Use public browsing for product evaluation by default; require explicit action-by-action consent before logged-in actions and stop before checkout, order submission, address handling, or payment.

Risk: The skill advertises a no-login boundary, but some documented workflows require an already logged-in Pinduoduo session.

Mitigation: Tell users when login is required, offer manual-mode alternatives, and keep final price, stock, delivery, coupons, and after-sales terms subject to user recheck before purchase.

## Reference(s):

- [Browser Workflow Guide](references/browser-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/pdd-shopping)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown shopping recommendations, seller-risk summaries, price comparisons, and user handoff steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize browser-visible product, seller, price, coupon, and order-preview evidence; payment remains user-controlled.]

## Skill Version(s):

2.2.0 (source: clawhub.json, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
