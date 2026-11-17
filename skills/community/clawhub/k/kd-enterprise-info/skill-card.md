## Description:

Accepts a company name, researches public business information across 11 dimensions with optional Tavily enhancement for registration, financial, and digital-system data, and generates a responsive Kingdee Lingjing-style HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kindeex](https://clawhub.ai/user/kindeex)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, presales, partner-review, competitive-analysis, and industry-research users use this skill to investigate a company from public sources and produce a structured business background report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local credential discovery and unsafe API-key handling may expose Tavily API keys in shared or sensitive workspaces.

Mitigation: Provide TAVILY_API_KEY only through an explicit environment variable and avoid placing unrelated secrets in .env files the skill can read.

Risk: Generated HTML reports may contain unescaped field content.

Mitigation: Do not host or redistribute generated reports unless the unescaped-field issue is fixed or the report is sanitized.

Risk: Public business-search results may be incomplete, stale, or inconsistent across sources.

Mitigation: Review source links and verify critical registration, financial, and business facts before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kindeex/skills/kd-enterprise-info)
- [Tavily Search API](https://tavily.com/)

## Skill Output:

**Output Type(s):** [Text, HTML, Configuration, Guidance]

**Output Format:** [Responsive HTML report with structured business sections and text guidance for optional search enhancement]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Missing fields are displayed as unavailable; financial data is shown only for listed companies when evidence is available.]

## Skill Version(s):

5.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
