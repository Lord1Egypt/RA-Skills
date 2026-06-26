## Description: <br>
Calculate true per-product profitability by mapping all cost layers \u2014 COGS, platform fees, payment processing, shipping, returns, and advertising \u2014 to reveal actual unit economics and identify margin leaks across an e-commerce catalog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce operators, analysts, and consultants use this skill to calculate SKU-level net contribution margin across marketplaces and direct-to-consumer channels. It helps identify margin-negative products, quantify cost leaks, and model practical improvement scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial recommendations can be misleading when cost inputs, fee schedules, advertising attribution, or return data are incomplete or stale. <br>
Mitigation: Require source documentation for each cost layer, flag estimates, verify current platform fee schedules, and include methodology notes and data limitations in the final report. <br>
Risk: Optimization scenarios such as category changes, packaging changes, supplier negotiation, or ad spend cuts may carry operational or policy tradeoffs. <br>
Mitigation: Model assumptions, implementation cost, timeline, and downside risk for each scenario before treating projected margin improvement as actionable. <br>
Risk: The release evidence includes capabilities related to crypto and purchases, which may be sensitive in some operating environments. <br>
Mitigation: Deploy only where those declared capabilities are acceptable, and keep human review over financial decisions or actions that could affect real spending. <br>


## Reference(s): <br>
- [Profit Margin Analyzer ClawHub release page](https://clawhub.ai/leooooooow/profit-margin-analyzer) <br>
- [Output template](references/output-template.md) <br>
- [Cost structure guide](references/cost-structure-guide.md) <br>
- [Margin optimization playbook](references/margin-optimization-playbook.md) <br>
- [Quality checklist](assets/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with tables, calculations, scenario summaries, and methodology notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-supplied cost, channel, return, and advertising data; financial outputs depend on source-data completeness and current fee schedules.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
