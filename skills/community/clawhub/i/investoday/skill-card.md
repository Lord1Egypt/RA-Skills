## Description:

Investoday provides financial data access, financial analysis, valuation analysis, fund performance attribution, and market broadcast workflows for A-shares, Hong Kong stocks, funds, and indices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cooperiano](https://clawhub.ai/user/cooperiano)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to retrieve market and financial data, assess company fundamentals and valuation, attribute fund performance, and draft market broadcast summaries. Outputs are informational and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned external Python package.

Mitigation: Install investoday-api only from a trusted package source, pin a reviewed version, and use a dedicated virtual environment.

Risk: Financial analysis and market summaries may be incomplete, stale, or unsuitable for a user's circumstances.

Mitigation: Treat outputs as informational only and verify financial decisions against authoritative sources and qualified advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cooperiano/skills/investoday)
- [Publisher Profile](https://clawhub.ai/user/cooperiano)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and prose analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial outputs are informational and depend on the external investoday-api package and its data sources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
