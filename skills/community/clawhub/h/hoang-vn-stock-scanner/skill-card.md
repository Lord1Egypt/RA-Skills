## Description:

Helps agents retrieve Vietnam stock market news from CafeF and basic ticker metrics from TCBS for VN-Index, HoSE, HNX, and UPCoM analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoanghust2003](https://clawhub.ai/user/hoanghust2003)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about Vietnamese equities by fetching CafeF market news and TCBS ticker metrics, then summarizing the likely market impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe command execution patterns.

Mitigation: Run the scanner with structured arguments and validate ticker and keyword inputs before execution.

Risk: The security evidence reports disabled TLS verification for financial data sources.

Mitigation: Restore TLS certificate verification and treat returned news and metrics as untrusted until that is fixed.

Risk: The security guidance notes path handling should be made package-relative.

Mitigation: Use package-relative paths so the skill does not depend on a publisher-specific local workspace path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hoanghust2003/skills/hoang-vn-stock-scanner)
- [CafeF market news RSS feed](https://cafef.vn/tin-tuc-su-kien.rss)
- [TCBS public ticker overview API](https://apipubaws.tcbs.com.vn/tcanalysis/v1/ticker/{ticker}/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional ticker and keyword inputs; returned news and metrics should be treated as untrusted until the noted security issues are remediated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
