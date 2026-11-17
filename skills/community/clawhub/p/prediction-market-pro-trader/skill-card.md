## Description:

Analyze Polymarket and Kalshi events using base rates and Bayesian updating to identify mispriced contracts and recommend value trades with risk controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xzahra](https://clawhub.ai/user/0xzahra)

### License/Terms of Use:

MIT-0

## Use Case:

External prediction-market analysts and traders use this skill to structure event research, estimate probabilities, compare those estimates with market prices, and form risk-controlled trade recommendations. Outputs should be treated as educational financial opinions requiring independent review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce explicit prediction-market trade recommendations and position sizes.

Mitigation: Require human review of every recommendation and prohibit agents from placing trades or sizing positions automatically.

Risk: Prediction-market trading may be restricted or unlawful in some jurisdictions.

Mitigation: Verify platform availability and legal compliance for the user's jurisdiction before acting on any analysis.

Risk: The skill presents financial opinions while also disclaiming that it is educational and not financial advice.

Mitigation: Treat outputs as high-risk educational analysis, independently validate sources and assumptions, and avoid risking funds the user cannot afford to lose.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xzahra/skills/prediction-market-pro-trader)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown report with probability estimates, evidence rationale, edge calculation, recommendation, confidence level, and position-size guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces actionable prediction-market trading opinions; human review is required before any trading decision.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
