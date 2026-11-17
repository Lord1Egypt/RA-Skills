## Description:

Retail promotion calculator and discount lookup for digital employees that computes final prices after discounts, bundles, thresholds, and membership tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangwei-frank](https://clawhub.ai/user/fangwei-frank)

### License/Terms of Use:

MIT-0

## Use Case:

Retail employees and customer-facing digital agents use this skill to answer promotion questions, calculate discounted cart totals, and explain savings from active offers. The skill depends on supplied promotion and membership configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Promotion totals can be wrong or unauthorized if applicability, stacking, input validation, or unsupported promotion types are incomplete.

Mitigation: Manually verify quoted totals before using them for orders, customer promises, refunds, or accounting, or fix and test the promotion logic before production use.

## Reference(s):

- [Promotion Engine ClawHub release page](https://clawhub.ai/fangwei-frank/skills/promotion-engine)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with calculation steps; helper script can emit JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calculations depend on supplied promotions[] knowledge base data and membership{} configuration; helper script output uses CNY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
