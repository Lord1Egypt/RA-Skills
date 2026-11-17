## Description:

Helps agents prepare Chinese-language intrinsic value worksheets using Graham, asset value, earnings value, and DCF methods with margin-of-safety and sensitivity analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this Chinese-language skill to compare intrinsic value estimates, calculate margin of safety, and structure sensitivity analysis from user-supplied financial assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Valuation outputs can be misleading if financial data or assumptions are stale, incomplete, or overly optimistic.

Mitigation: Require users to provide reliable current data, review all growth and discount-rate assumptions, and treat buy or observe labels as analytical aids rather than trading instructions.

Risk: The skill may be mistaken for professional investment advice because it produces margin-of-safety calculations and recommendation labels.

Mitigation: Present results as a worksheet for further review and pair them with independent research, moat analysis, and human judgment before any investment decision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lj22503/skills/intrinsic-value-calculator)
- [Publisher Profile](https://clawhub.ai/user/lj22503)
- [Valuation Methods Reference](references/valuation-methods.md)
- [Valuation Template](templates/valuation-template.md)
- [Maotai Valuation Example](examples/maotai-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown valuation worksheet with formulas, tables, and optional JSON-style result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied financial data and current assumptions; no code execution, persistence, credential use, or hidden data movement identified.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
