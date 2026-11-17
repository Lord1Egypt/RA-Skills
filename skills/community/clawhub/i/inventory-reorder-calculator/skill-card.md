## Description:

Estimate ecommerce reorder timing and quantity using demand, lead time, and safety stock assumptions so teams can set reorder points and reduce stockout risk with less guesswork.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce operators, buyers, founders, and inventory teams use this skill to calculate reorder points and purchase quantities for SKUs or product groups. It helps turn demand, lead-time, safety-stock, MOQ, cash, and storage assumptions into an actionable reorder recommendation with visible tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reorder recommendations can affect purchasing decisions, stockout exposure, and cash flow.

Mitigation: Review assumptions, formulas, supplier inputs, cash constraints, and final quantities before acting on the recommendation.

Risk: Weak demand history, supplier quotes, or unmodeled lead-time variability can make the calculated reorder point fragile.

Mitigation: Flag low-confidence inputs, account for demand and lead-time variability, and recalculate when demand shifts, supplier lead time changes, promotions occur, or stockouts happen.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leooooooow/skills/inventory-reorder-calculator)
- [Demand Analysis Guide for Reorder Planning](references/demand-analysis-guide.md)
- [Safety Stock Guide](references/safety-stock-guide.md)
- [Inventory Reorder Calculator Output Template](references/output-template.md)
- [Reorder Recommendation Quality Checklist](assets/reorder-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown with tables, formulas, action items, and review triggers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows assumptions, demand and lead-time models, safety stock, reorder point, reorder quantity, risk scenarios, and recalculation triggers.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
