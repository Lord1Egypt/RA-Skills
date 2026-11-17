## Description:

Calculates Amazon FBA product profitability from seller-provided costs, including cost breakdowns, net margins, break-even prices, pricing recommendations, and batch SKU summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and e-commerce operators use this skill to estimate FBA profitability, compare single products or batches of SKUs, and reason about pricing changes before sourcing or listing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The global npx installation command is unpinned.

Mitigation: Prefer a pinned or reviewed source before installation.

Risk: Profitability outputs are estimates and depend on accurate seller-provided inputs and static fee assumptions.

Mitigation: Validate inputs and compare results against current Amazon fees or other business records before making financial decisions.

Risk: Limited input validation may allow malformed values to produce errors or misleading calculations.

Mitigation: Check required numeric fields before running analyses and review outputs for reasonableness.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phheng/skills/profit-margin-calculator-amazon)
- [Amazon Skills collection](https://github.com/nexscope-ai/Amazon-Skills)
- [eCommerce Skills collection](https://github.com/nexscope-ai/eCommerce-Skills)
- [Nexscope](https://nexscope.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with tables, cost breakdowns, break-even analysis, pricing recommendations, and optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are estimates based on user-provided costs and static referral or fee assumptions; no API key is required.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
