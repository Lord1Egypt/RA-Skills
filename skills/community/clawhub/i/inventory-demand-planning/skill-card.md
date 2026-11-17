## Description:

Provides inventory demand planning guidance for forecasting, safety stock calculation, replenishment planning, promotional lift estimation, ABC/XYZ analysis, seasonal transition management, and vendor negotiation at multi-location retailers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nocodemf](https://clawhub.ai/user/nocodemf)

### License/Terms of Use:

Apache-2.0

## Use Case:

Retail demand planners, supply chain teams, and inventory operators use this skill to choose forecasting methods, calculate safety stock, plan replenishment, estimate promotional impact, and prepare vendor or merchandising recommendations across multi-location assortments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inventory recommendations could affect purchase orders, stock records, markdowns, liquidation decisions, vendor communications, or public statements if applied directly.

Mitigation: Use the skill as decision support and require explicit human approval before any live business or system-of-record action.

Risk: The evaluation runner imports a shared framework path from the surrounding repository.

Mitigation: Run artifact/evals/run_evals.py only when the surrounding repository and imported shared framework are trusted.

Risk: Safety stock was the weakest evaluated category despite overall passing results.

Mitigation: Review safety stock calculations and assumptions carefully, especially for intermittent demand, lead time variability, and high-service-level scenarios.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nocodemf/skills/inventory-demand-planning)
- [Decision Frameworks - Inventory Demand Planning](artifact/references/decision-frameworks.md)
- [Inventory Demand Planning - Edge Cases Reference](artifact/references/edge-cases.md)
- [Communication Templates - Inventory Demand Planning](artifact/references/communication-templates.md)
- [Inventory Demand Planning - LLM Grading Rubric](artifact/evals/rubric.md)
- [Evaluation Results](artifact/evals/results/eval_results.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with calculations, decision tables, and communication templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision-support content; human approval is required before live inventory, purchase order, markdown, liquidation, vendor communication, or system-of-record changes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
