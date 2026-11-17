## Description:

Scan ecommerce inventory notes or CSV exports for stockout, overstock, aging, inbound-delay, and promo-readiness risk, then turn them into a ranked watchlist, days-of-cover summary, action ladder, scenario notes, and operator-ready meeting brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Inventory planners, operations leads, finance-aware operators, founders, and marketplace teams use this skill to turn supplied inventory, sales, and supplier notes into a practical risk brief for stockout, overstock, aging, inbound-delay, and promotion-readiness review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The brief may overstate confidence when inventory, velocity, lead-time, margin, or SKU mapping inputs are incomplete.

Mitigation: Treat exposure estimates as directional, reduce confidence for weak inputs, and verify assumptions against source inventory records before acting.

Risk: Operational decisions such as purchase orders, transfers, markdowns, liquidation, or promotion changes could affect revenue, cash, or customer experience.

Mitigation: Keep final replenishment, liquidation, promotion, and purchasing decisions under human review.

Risk: Users may assume the skill has live ERP, WMS, supplier, or forecasting-system access.

Mitigation: Make clear that the skill only analyzes user-provided notes or exports and does not access live business systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/inventory-risk-radar)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown risk brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an inventory risk dashboard, days-of-cover summary, tiered watchlist notes, action ladder, scenario notes, assumptions, confidence notes, and limits.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
