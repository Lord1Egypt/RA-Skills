## Description:

Browser-first grocery price finder for mainland China that compares vegetables and everyday fresh groceries across Duoduo Maicai, Meituan Maicai, 7FRESH, Hema Fresh, Dingdong Maicai, and similar platforms, normalizes city-specific basket cost, delivery or pickup friction, freshness tradeoffs, and coupon thresholds, and tells the user where to buy the cheapest useful basket right now.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to compare public mainland China grocery prices and decide the cheapest useful basket, platform, or ingredient route after normalizing coupons, fees, pickup friction, freshness, and city-specific availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public grocery prices can be city-, warehouse-, and time-specific, so a stale or location-mismatched comparison can mislead the user.

Mitigation: Timestamp live judgments, state the city or say the result is directional, and ask for city and basket details when they are missing.

Risk: Private account pricing, coupon claiming, payment, and order placement would exceed the intended public-price comparison boundary.

Mitigation: Use only public listings or user-provided screenshots and stop before login, coupon claiming, payment, or irreversible cart submission.

Risk: Lowest visible prices may depend on thresholds, add-on items, pickup friction, packaging fees, delivery fees, weaker freshness, or smaller specifications.

Mitigation: Normalize total payable basket cost, unit weight, fees, thresholds, pickup or delivery friction, and freshness confidence before recommending a route.

## Reference(s):

- [Maicai ClawHub skill page](https://clawhub.ai/harrylabsj/skills/maicai)
- [Normalization Rules](references/normalization-rules.md)
- [Platform Lenses](references/platform-lenses.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with direct recommendations, basket comparisons, price rationale, risk warnings, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should timestamp live judgments, identify the city when known, and avoid private account pricing or checkout actions.]

## Skill Version(s):

1.0.0 (source: frontmatter, clawhub.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
