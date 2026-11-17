## Description:

Walmart profit margin calculator for sellers. Calculate cost breakdowns including WFS fulfillment, storage fees, and referral fees. Includes comparison with Amazon FBA and lower competition advantage analysis. No API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and ecommerce operators can ask an agent to estimate product profitability, cost breakdowns, break-even pricing, and marketplace margin comparisons for Walmart-focused selling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged suspicious because the documentation presents a Walmart/WFS calculator while the shipped calculator logic is Amazon/FBA-oriented.

Mitigation: Review the implementation against Walmart/WFS fee requirements before relying on results for profitability decisions.

Risk: The documented installation command uses an unpinned global npx install.

Mitigation: Prefer a pinned, project-local install from an immutable reviewed source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phheng/skills/profit-margin-calculator-walmart)
- [Nexscope AI](https://www.nexscope.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports and inline shell commands, with Python code supplied by the artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May accept JSON product input for single-product or batch margin analysis.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
