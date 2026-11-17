## Description:

Portfolio Dehydrator diagnoses hidden overlap in Web3 portfolios, fetches public crypto market data, runs constrained risk-adjusted optimization, and produces allocation recommendations and client-facing reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaozrrr](https://clawhub.ai/user/shaozrrr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and portfolio-analysis agents use this skill to build or run a Web3 portfolio optimizer that identifies redundant exposure, compares downside-adjusted metrics, and generates actionable rebalancing guidance from real market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried token symbols are sent to public exchange APIs.

Mitigation: Pass only normalized token symbols and optional allocation weights; do not provide wallet private keys.

Risk: Python dependencies are listed without pinned versions.

Mitigation: Install in a virtual environment or container and pin dependency versions before production deployment.

Risk: Portfolio recommendations depend on available historical market data and may degrade during rate limits, bad tickers, or exchange outages.

Mitigation: Review data-confidence labels, skipped-asset warnings, and cash-buffer recommendations before acting on the report.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shaozrrr/skills/portfolio-dehydrator)
- [Source Repository](https://github.com/Shaozrrr/portfolio-dehydrator-skill)
- [Implementation Spec](references/implementation-spec.md)
- [Bundled Backend](assets/web3_portfolio_optimizer.py)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and requirements code blocks; the bundled backend emits Chinese Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public exchange market data and degrades to partial or cash-only recommendations when real data is unavailable.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
