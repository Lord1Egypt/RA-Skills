## Description: <br>
JD.com shopping assistant. Input a JD product name or link; output self-operated/flagship trust checks, visible price, review risks, SKU recommendation, and cart-ready summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping agents use this skill to research JD.com products, compare seller trust and visible prices, select SKUs, and prepare a cart while leaving login, checkout, order confirmation, and payment to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security guidance flags workflow helpers that can affect accounts, public content, production data, or send code diffs to configured AI providers when explicitly invoked. <br>
Mitigation: Install only when those ClawHub, Convex, moderation, email, migration, or autoreview workflows are expected, and review those actions before use. <br>
Risk: Shopping browser workflows may expose account, address, invoice, payment, or checkout surfaces. <br>
Mitigation: Keep login, identity checks, address selection, checkout, order confirmation, and payment user-only; stop at the product page or cart page and redact personal details in summaries by default. <br>
Risk: Visible prices, coupons, stock, delivery, and seller terms can change before settlement. <br>
Mitigation: Treat public and cart-visible values as decision inputs, and require the user to recheck final payable amount, eligibility, address-dependent delivery, and payment terms during manual checkout. <br>


## Reference(s): <br>
- [Browser Workflow Guide](artifact/references/browser-workflow.md) <br>
- [Output Patterns](artifact/references/output-patterns.md) <br>
- [Platform Fit](artifact/references/platform-fit.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/jd-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with product comparison tables, recommendation summaries, caveats, and cart-ready handoff notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize browser-visible prices, seller signals, review risks, SKU selections, and cart contents; final price, checkout, order confirmation, and payment remain user-controlled.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
