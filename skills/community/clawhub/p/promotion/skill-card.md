## Description:

Cross-platform promotion radar for mainland China shopping platforms that tracks the hottest current campaigns across Taobao, Tmall, JD, PDD, VIPSHOP, and similar marketplaces, ranks them by real savings, participation friction, category fit, freshness, and urgency, and tells the user which promotions are actually worth chasing right now.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to scan mainland China e-commerce promotions, compare platform mechanics, and decide which campaigns or categories are worth checking now. It is intended for public promotion analysis, not account-specific shopping automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Promotion status, prices, inventory, and coupon eligibility can change quickly or vary by user.

Mitigation: Timestamp live checks, separate confirmed from inferred status, and have users verify final payable price and activity terms on public platform pages before acting.

Risk: Shopping workflows can expose private account state or move toward coupon claiming and purchases.

Mitigation: Use only public campaign and category pages, and stop before login, coupon claiming, cart submission, or ordering.

Risk: The skill uses China-market framing and Chinese-style deal analysis that may not fit other regions or languages.

Mitigation: Ask users to specify another language or non-China platform scope when they need different market coverage.

## Reference(s):

- [Promotion Skill Page](https://clawhub.ai/harrylabsj/skills/promotion)
- [Promotion Repository](https://github.com/harrylabsj/promotion)
- [Platform Promo Patterns](references/promo-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamped promotion analysis, ranked recommendations, category shortcuts, and action-oriented caveats based on public shopping-platform signals.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
