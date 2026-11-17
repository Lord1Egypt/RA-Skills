## Description:

Computes portfolio risk and exposure metrics before sizing and rebalance decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compute portfolio volatility, drawdown, benchmark sensitivity, concentration, correlation, confidence, and data-gap metrics from local holdings and price-history CSV files before sizing or rebalance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio analytics may be mistaken for trade instructions or investment advice.

Mitigation: Use the output as risk-management context only and review results before making sizing, rebalance, or financial decisions.

Risk: Incomplete, stale, or misaligned holdings, price, benchmark, sector, or liquidity data can produce misleading metrics.

Mitigation: Validate required columns, aligned dates, complete weights, and the confidence and data-gap sections before relying on the metrics.

Risk: The skill reads user-provided portfolio CSVs and writes a local JSON summary.

Mitigation: Provide only intended local files and review the generated output directory contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teahann/skills/portfolio-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown analysis with shell command guidance and a local JSON summary file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided local CSV inputs for holdings and price history; optional benchmark data enables beta and relative-risk metrics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
