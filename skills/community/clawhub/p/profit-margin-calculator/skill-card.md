## Description:

Calculate true ecommerce profit margin after product cost, shipping, platform fees, discounts, and refund drag.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and analysts use this skill to compare SKU profitability, validate pricing room, and diagnose why revenue growth is not converting into profit. It guides margin-scope clarification before calculating gross profit, net profit, margin drags, improvement ideas, and a reusable Python script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Margin results can be incorrect or misleading if the user supplies incomplete cost inputs or mixes gross, contribution, and net margin definitions.

Mitigation: Confirm the margin definition and required inputs before calculating, and clearly label assumptions and estimated values in the output.

Risk: Financial calculations may be treated as precise even when refund drag, discounts, platform fees, or fixed-cost allocations are estimates.

Mitigation: Show formulas, assumptions, and the largest margin drags so users can review the calculation basis before making pricing or operating decisions.

## Reference(s):

- [Profit Margin Calculator Output Template](artifact/references/output-template.md)
- [Profit Margin Calculator on ClawHub](https://clawhub.ai/leooooooow/skills/profit-margin-calculator)

## Skill Output:

**Output Type(s):** [Markdown, Code, Guidance]

**Output Format:** [Markdown with tables, calculation results, recommendations, and Python code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided pricing, cost, fee, discount, refund, and optional fixed-cost inputs; asks follow-up questions when margin scope or inputs are incomplete.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
