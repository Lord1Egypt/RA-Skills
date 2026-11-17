## Description:

Audit ecommerce inventory notes or SKU exports, flag stockout, aging, overstock, capital lock-up, and promo-readiness risks, then turn partial inventory data into a prioritized replenish-hold-clear brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, buyers, planners, and founders use this skill to turn SKU notes, inventory exports, sales velocity, lead times, and campaign context into a practical inventory health brief for weekly or monthly reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces heuristic inventory guidance from user-provided data and may be misleading when sales velocity, lead time, campaign timing, or seasonality context is incomplete.

Mitigation: Treat the report as an advisory brief, downgrade certainty for incomplete signals, and verify recommendations against current business records before acting.

Risk: Inventory recommendations could influence replenishment, purchasing, markdown, or clearance decisions with financial impact.

Mitigation: Keep replenishment quantities, purchase orders, markdowns, and clearance actions human-approved.

Risk: Users may provide more sensitive SKU, sales, supplier, campaign, or cash context than needed for the report.

Mitigation: Provide only the SKU, sales, lead-time, campaign, and business context needed for the requested inventory review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/inventory-health-auditor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an inventory health summary, priority queue, recommended actions, 30-day action plan, assumptions, evidence gaps, and limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
