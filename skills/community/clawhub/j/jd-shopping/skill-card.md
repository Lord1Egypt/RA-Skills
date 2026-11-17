## Description:

JD.com shopping assistant. Input a JD product name or link; output self-operated/flagship trust checks, visible price, review risks, SKU recommendation, and cart-ready summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare JD.com products, assess seller trust and review risks, choose SKUs, and prepare cart contents before they personally handle checkout and payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse JD.com and change cart contents in a logged-in user session after confirmation.

Mitigation: Require explicit user confirmation before SKU, coupon, quantity, cart-add, cart-remove, or other account-state changes.

Risk: Checkout, payment, address, invoice, coupon eligibility, stock, delivery, and final payable amount can change after cart preparation.

Mitigation: Stop before checkout and direct the user to personally review login, CAPTCHA, address, invoice, settlement, final confirmation, payment, and final price.

Risk: Logged-in shopping pages may expose personal account, address, cart, or payment information.

Mitigation: Avoid storing cookies, credentials, account data, payment data, addresses, cart data, or order data outside the active browser session and redact personal details in summaries by default.

## Reference(s):

- [Platform Fit](references/platform-fit.md)
- [Output Patterns](references/output-patterns.md)
- [Browser Workflow Guide](references/browser-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/jd-shopping)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown with comparison tables, recommendations, caveats, and cart-ready summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses visible JD.com and user-provided information; final price, stock, delivery, coupons, and payment remain user-verified.]

## Skill Version(s):

2.1.1 (source: server release metadata; package.json and clawhub.json list 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
