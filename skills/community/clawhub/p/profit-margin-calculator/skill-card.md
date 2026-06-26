## Description: <br>
Calculate true ecommerce profit margin after product cost, shipping, platform fees, discounts, and refund drag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leooooooow](https://clawhub.ai/user/Leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external ecommerce operators, and analysts use this skill to calculate gross, contribution, or net margin for products and SKUs. It helps identify cost, fee, discount, refund, fulfillment, and fixed-cost drag before pricing decisions or business reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Margin outputs can be misleading if gross, contribution, and net margin are mixed or required cost categories are omitted. <br>
Mitigation: Confirm the requested margin definition, included costs, formulas, and assumptions before calculating, and label estimated values. <br>
Risk: Generated Python code could contain calculation or handling errors if run without review. <br>
Mitigation: Review any generated Python script before running it and provide only the sales and cost numbers needed for the calculation. <br>


## Reference(s): <br>
- [Profit Margin Calculator Output Template](references/output-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/Leooooooow/profit-margin-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with cost tables, margin calculations, recommendations, and optional Python code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Clarifies margin definitions and assumptions before calculation; labels estimated values when inputs are incomplete.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
