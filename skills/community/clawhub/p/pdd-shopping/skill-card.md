## Description: <br>
PDD Shopping Assistant helps an agent assess Pinduoduo products or links by comparing subsidy and group-buy prices, seller risk, visible prices, review signals, refund caveats, and purchase boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to research Pinduoduo shopping options, compare group-buy and subsidy mechanics, evaluate seller trust signals, and prepare a purchase summary. Login-required cart, coupon, group-buy, and checkout-preview actions require close user supervision and final purchase steps remain manual. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill description says no login, while the artifact includes login-required cart, group-buy, coupon, and checkout-preview flows. <br>
Mitigation: Require explicit user consent before any login-required step, supervise each browser action, and keep final checkout, order submission, and payment manual. <br>
Risk: Shopping automation may expose sensitive account session, address, coupon, cart, or order-preview information. <br>
Mitigation: Do not enter credentials, SMS codes, CAPTCHA responses, identity checks, addresses, or payment details for the user; use only browser-visible or user-provided information. <br>
Risk: Product prices, stock, subsidy eligibility, seller ratings, reviews, and after-sales terms can be stale or misleading. <br>
Mitigation: Capture current page evidence, warn on weak seller or review signals, and require the user to recheck final price, stock, delivery, coupons, and after-sales terms before purchase. <br>


## Reference(s): <br>
- [Browser Workflow Guide](references/browser-workflow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/pdd-shopping) <br>
- [Pinduoduo Mobile Site](https://mobile.yangkeduo.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with shopping comparisons, checklists, browser-observation summaries, and manual handoff steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include visible product, seller, coupon, cart, and order-preview observations; payment and final order submission remain outside the agent output.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata, clawhub.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
