## Description:

Household replenishment planning skill for mainland China that turns pantry status, weekly menu, repeat-purchase habits, and recent consumption clues into a cross-platform home supply system across Meituan, PDD, Taobao, Meituan Maicai, Duoduo Maicai, and similar channels, estimates what is running low, routes urgent top-ups versus stock-up buys versus long-tail one-offs, and outputs the cheapest, fastest, and lowest-friction restock plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn household inventory, weekly menus, repeat-purchase patterns, and recent order clues into actionable restock plans. It separates urgent top-ups, weekly groceries, stock-up items, long-tail one-offs, and do-not-buy items across China-market commerce channels.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Household inventory, menus, screenshots, and order history can reveal personal routines or purchasing patterns.

Mitigation: Share only the household context needed for the restock plan and omit sensitive account, payment, or private order details unless intentionally provided.

Risk: The skill may estimate depletion or platform suitability from incomplete user-provided information.

Mitigation: Label assumptions and confidence levels, and treat uncertain inventory or consumption signals as planning estimates rather than facts.

Risk: Commerce actions such as login, coupon claiming, checkout, and payment are irreversible or account-sensitive.

Mitigation: Keep account access, coupon claiming, order submission, and payment under the user's direct control.

## Reference(s):

- [PantryPilot Skill Page](https://clawhub.ai/harrylabsj/skills/pantrypilot)
- [Publisher Profile](https://clawhub.ai/user/harrylabsj)
- [Replenishment Framework](references/replenishment-framework.md)
- [Platform Routing](references/platform-routing.md)
- [Output Patterns](references/output-patterns.md)
- [Example Prompts](references/example-prompts.md)
- [Test Cases](references/test-cases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style replenishment plans with item buckets, platform routing, three plan variants, do-not-buy notes, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions and confidence labels when inventory, prices, stock, or delivery timing are incomplete.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
