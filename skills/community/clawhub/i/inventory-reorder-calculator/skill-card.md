## Description: <br>
Estimate ecommerce reorder timing and quantity using demand, lead time, and safety stock assumptions so teams can set reorder points and reduce stockout risk with less guesswork. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators, buyers, founders, and operations teams use this skill to estimate reorder points and reorder quantities for SKUs or product groups using demand, lead-time, safety-stock, and constraint assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inventory recommendations can be wrong if demand data, supplier lead times, MOQs, cash limits, or other assumptions are stale or inaccurate. <br>
Mitigation: Use the skill as a planning aid and verify inputs against business records before acting on a reorder recommendation. <br>
Risk: Numeric reorder outputs can appear more precise than the underlying assumptions support. <br>
Mitigation: Review confidence levels, scenario tables, sensitivity warnings, and recalculation triggers before using the recommendation. <br>


## Reference(s): <br>
- [Demand Analysis Guide for Reorder Planning](references/demand-analysis-guide.md) <br>
- [Inventory Reorder Calculator Output Template](references/output-template.md) <br>
- [Safety Stock Guide](references/safety-stock-guide.md) <br>
- [Reorder Recommendation Quality Checklist](assets/reorder-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown with assumptions, calculations, tables, action items, and review triggers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should show formulas, assumptions, confidence levels, risk scenarios, and concrete reorder actions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
