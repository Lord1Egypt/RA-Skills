## Description:

Provides structured U.S. stock holding analysis and trade guidance using current market, macro, sector, social, insider-flow, technical, and risk-control signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonxu](https://clawhub.ai/user/canonxu)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and portfolio-review agents use this skill to structure U.S. equity portfolio reviews from text or screenshots, compare holdings against current market conditions, and produce risk-aware allocation and trade-action tables for user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store holdings, cost basis, total capital, and other portfolio details in a local portfolio snapshot.

Mitigation: Use it only with portfolio data you are comfortable storing locally, protect or remove ~/.openclaw/memory/portfolio.json after use, and avoid sharing account identifiers or unnecessary personal data.

Risk: Trade actions and allocation tables can be mistaken for personalized financial advice.

Mitigation: Treat outputs as analysis for review, validate market data and assumptions independently, and consult a qualified financial professional before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canonxu/skills/my-stock-analysis-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables and narrative analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request missing portfolio fields, cite data sources in outputs, and save a local portfolio snapshot for later analysis.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
