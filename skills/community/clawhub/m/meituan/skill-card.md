## Description: <br>
Meituan public local-life decision assistant. Compare visible merchant, fee, discount, ETA, review-risk, threshold, and refund-friction signals, then recommend whether to order, switch, add a useful item, wait, or skip. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and coding agents use this skill to compare public Meituan food-delivery or local-life deal evidence and choose a practical next action before ordering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private account, address, coupon, order, checkout, or payment details could be exposed if the skill is used on authenticated Meituan pages. <br>
Mitigation: Use only public pages, screenshots, or user-provided visible details, and have the user personally verify final price, ETA, stock, refund terms, and payment details before ordering. <br>
Risk: Recommendations based on visible prices, fees, ETA, stock, or coupons can become stale before checkout. <br>
Mitigation: Present the recommendation as decision support and call out final payable amount, address-based ETA, account coupon eligibility, item options, stock, and refund terms as manual checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/meituan) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/harrylabsj) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, analysis] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a concise recommendation with checkout reality, risk check, confidence gaps, and user-only checks before ordering.] <br>

## Skill Version(s): <br>
2.2.0 (source: server evidence, SKILL.md frontmatter, package.json, clawhub.json, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
