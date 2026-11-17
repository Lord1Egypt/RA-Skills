## Description:

Analyzes user-provided stock and ETF portfolio screenshots across technical, capital-flow, and fundamental signals, then provides portfolio actions and new candidate recommendations for A-share, Hong Kong, ETF, and fund markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tingdall](https://clawhub.ai/user/tingdall)

### License/Terms of Use:

MIT-0

## Use Case:

External investors and portfolio reviewers use this skill to analyze user-provided holdings screenshots for A-share, Hong Kong, ETF, and fund portfolios. It turns current market research into markdown reports with position-level ratings, overall allocation guidance, risk notes, and replacement or watchlist candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio screenshots may contain account numbers, broker identifiers, or personal details.

Mitigation: Redact sensitive account, broker, and personal information before uploading screenshots for analysis.

Risk: Portfolio ratings and candidate recommendations may be over-relied upon as personalized financial advice.

Mitigation: Treat outputs as research support only and validate decisions with independent judgment or a licensed financial professional.

Risk: Market data may be stale, intraday, or mixed across different report dates.

Mitigation: Use multiple independent sources, verify timestamps, prefer closing data when relevant, and disclose unresolved data conflicts in the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tingdall/skills/portfolio-management)
- [Analysis framework](artifact/analysis-framework.md)
- [Data verification guide](artifact/data-verification-guide.md)
- [Report template](artifact/report-template.md)
- [Stock screening guide](artifact/stock-screening-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown portfolio analysis reports with tables, ratings, position guidance, risk notes, and candidate recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use user-uploaded holdings screenshots and current market data; reports are expected to include source timestamps and financial-risk disclaimers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
