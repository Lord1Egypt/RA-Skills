## Description:

PriceTide is a mainland China shopping timing skill that judges whether a current product price is a short-term low, a fair buy, a wait candidate, or not worth chasing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping assistants use this skill to decide whether to buy a specific product now, wait, watch the next promotion event, or stop chasing the current price. It is focused on mainland China shopping channels and converts price clues, promotion rhythm, urgency, and waiting cost into a direct action recommendation.

### Deployment Geography for Use:

Global; designed for mainland China shopping scenarios.

## Known Risks and Mitigations:

Risk: The packaged publish script may execute an external validator path before publishing.

Mitigation: Do not run the publish script unless you are a maintainer in a trusted workspace and have verified or removed that validator path.

Risk: Shopping timing advice can become stale quickly when live prices, coupons, stock, or campaign stages change.

Mitigation: Anchor recommendations to an exact snapshot date and separate visible facts from directional timing inferences.

Risk: The skill could be misused to act on account-only discounts, coupon claims, reminders, checkout, or payment flows.

Mitigation: Keep agent activity limited to public product pages, campaign pages, screenshots, and price clues; the user should handle private-account actions and purchases.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/pricetide)
- [Publisher Profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with a Chinese verdict, concise timing rationale, buy-or-wait tradeoff, trigger, and next step]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usually converges to one of four verdicts: 现在买, 等等看, 先关注，等活动, or 不值得追这个价.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG.md, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
