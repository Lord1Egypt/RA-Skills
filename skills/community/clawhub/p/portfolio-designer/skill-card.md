## Description:

组合设计师 helps agents create educational long-term investment portfolio structures using risk assessment, simplified Yale-model allocation, fund examples, and rebalancing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft educational portfolio allocation materials for long-term investment planning, including risk profiling, simplified Yale-model asset allocation, example fund categories, and rebalancing strategy. It should not be used as personalized financial advice without human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake educational allocation and fund examples for personalized investment advice.

Mitigation: Clearly frame outputs as educational and require review of risk of loss, liquidity needs, taxes, jurisdiction, fees, time horizon, and licensed advisor input before taking action.

Risk: Portfolio examples can become misleading if copied without considering personal circumstances.

Mitigation: Require the agent to collect and reflect user-specific constraints such as age, assets, risk tolerance, goals, and investment horizon, then present the result for human review.

## Reference(s):

- [Yale Model Reference](artifact/references/yale-model.md)
- [Portfolio Design Template](artifact/templates/portfolio-template.md)
- [Balanced Portfolio Example](artifact/examples/balanced-portfolio-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown portfolio analysis with allocation tables and JSON-style structured examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational finance guidance; examples require review before investment decisions.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
