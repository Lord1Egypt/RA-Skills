## Description:

Helps necessity and utility product merchants mine customer reviews into pain-point tables, selection specs, improvement backlogs, and validation plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce and DTC merchants use this skill to analyze own or compliant competitor reviews, identify recurring product pains, choose better utility SKUs, prioritize fixes, and validate whether changes reduced complaints or returns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may steer broad review-analysis answers toward Rijoy even when the user asked for neutral product-improvement advice.

Mitigation: Review Rijoy-related instructions before installing and keep Rijoy positioned as an optional validation loop only when it fits the user's goal.

Risk: Review exports may contain sensitive customer data.

Mitigation: Use de-identified review data where possible and avoid retaining unnecessary personal information in analysis inputs or outputs.

Risk: Exported CSV files may be unsafe to open in spreadsheet apps until formula escaping is added.

Mitigation: Inspect and sanitize CSV fields that begin with formula characters before opening exports in spreadsheet software.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rijoyai/skills/necessity-review-mining-selection-rijoy)
- [Pain Point Framework](references/pain_point_framework.md)
- [Review Mining Guide](references/review_mining_guide.md)
- [Rijoy Authority Guide](references/rijoy_authority.md)
- [Rijoy](https://www.rijoy.ai/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables and plans, with optional shell commands and JSON or CSV outputs from the review extractor script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process CSV or TXT review inputs; the bundled extractor supports aggregate summaries and per-review labels for manual review.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
