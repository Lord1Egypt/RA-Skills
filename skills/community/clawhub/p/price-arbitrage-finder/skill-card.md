## Description:

Finds cross-platform product price differences across Taobao, JD.com, and Pinduoduo and calculates arbitrage profit after shipping costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[275254cl-hash](https://clawhub.ai/user/275254cl-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and commerce operators use this skill to compare prices across Chinese e-commerce platforms, sort arbitrage opportunities by profit rate, monitor price changes, and set profit reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The requests dependency is disclosed but unpinned.

Mitigation: Install from a controlled environment and pin or lock the dependency before production use.

Risk: Arbitrage suggestions may omit marketplace rules, shipping, commission, authenticity, after-sales, or price-volatility constraints.

Mitigation: Review platform policies and total landed costs before acting on any opportunity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/275254cl-hash/skills/price-arbitrage-finder)
- [Artifact homepage](https://github.com/openclaw/skills)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown text with product comparisons, profit calculations, ranked opportunities, monitoring prompts, and cautions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact declares a python3 runtime requirement and a requests pip dependency.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
