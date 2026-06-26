## Description: <br>
Chinese-language skill that calculates promotion pricing, profit margins, breakeven points, and SKU-level discount comparisons before a campaign decision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators, merchandisers, and business analysts use this skill to compare discount plans, estimate gross and net margin, calculate breakeven points, and decide whether a promotion is financially viable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Promotion recommendations depend on user-supplied costs and reference assumptions; stale fees, return rates, or sales uplift estimates can mislead profit decisions. <br>
Mitigation: Verify platform fees, return rates, sales uplift, and cost inputs against current internal or platform data before making business decisions. <br>
Risk: Batch CSV calculations may expose SKU-level cost and sales assumptions if unnecessary business data is included. <br>
Mitigation: Use local CSV files containing only the SKU and cost fields needed for the calculation, and avoid adding credentials or unrelated customer data. <br>


## Reference(s): <br>
- [Cost Structure Reference Template](references/cost-structure.md) <br>
- [Main E-commerce Platform Fee Reference](references/platform-fees.md) <br>
- [Promotion Effect Coefficient Reference](references/promo-effect.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with calculator output tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use local CSV input for batch SKU calculations; no network access or credential use is indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
