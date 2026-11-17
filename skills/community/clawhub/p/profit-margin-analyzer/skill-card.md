## Description:

Calculate true per-product profitability by mapping all cost layers - COGS, platform fees, payment processing, shipping, returns, and advertising - to reveal actual unit economics and identify margin leaks across an e-commerce catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, analysts, and advisors use this skill to build SKU-level profitability reports, identify margin leaks across channels, and model improvement scenarios with dollar-impact estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business exports used for margin analysis may contain sensitive sales, cost, or supplier information.

Mitigation: Provide only the exports needed for the report and avoid sharing account credentials, session data, or unrelated confidential records.

Risk: Marketplace, payment, shipping, and advertising fee schedules can change, which may make margin recommendations inaccurate.

Mitigation: Verify current fee schedules and rate cards before relying on the financial recommendations.

Risk: Scenario outputs may overstate savings if assumptions such as COGS reductions, return-rate improvements, or advertising changes are not achievable.

Mitigation: Review assumptions, implementation costs, tradeoffs, and current business constraints before acting on proposed margin improvements.

## Reference(s):

- [Output Template](references/output-template.md)
- [E-Commerce Cost Structure Guide](references/cost-structure-guide.md)
- [Margin Optimization Playbook](references/margin-optimization-playbook.md)
- [Profit Margin Analysis Quality Checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis report with tables, calculations, scenario summaries, methodology notes, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided business exports and fee schedules; recommendations depend on current marketplace, payment, shipping, and advertising data.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
