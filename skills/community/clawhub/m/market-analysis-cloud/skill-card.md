## Description:

Orchestrates a cloud-only daily A-share market analysis workflow covering trading calendar checks, market data, news, portfolio and watchlist diagnostics, ERP calculation, report assembly, and IMA knowledge-base upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyyy10000yyyy](https://clawhub.ai/user/yyyy10000yyyy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to generate daily A-share market research reports from market data, news, portfolio holdings, watchlists, and equity risk premium signals. It is intended to coordinate dependent data skills and produce a structured report plus a short upload confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow exposes an API key in the skill text.

Mitigation: Remove the embedded key, rotate it, and require users to provide their own key through a secure environment-variable mechanism.

Risk: The workflow can read holdings and watchlist data and store a detailed portfolio-derived report in IMA without clear per-run consent.

Mitigation: Add explicit user confirmation before reading portfolio folders or uploading generated reports, and document what portfolio-derived data is stored.

Risk: The workflow depends on multiple external market-data skills and web searches whose outputs may be incomplete, stale, or unavailable.

Mitigation: Pin or verify dependencies where possible and require the generated report to identify missing or fallback data before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yyyy10000yyyy/skills/market-analysis-cloud)
- [stock-price-query-mx dependency](https://clawhub.ai/skills/stock-price-query-mx)
- [tecent-finance dependency](https://clawhub.ai/skills/tecent-finance)
- [eastmoney-mx-skills-suite dependency](https://clawhub.ai/kooui/skills/eastmoney-mx-skills-suite)
- [china-stock-data dependency](https://longxiaskill.com/skill/china-stock-data)
- [Eastmoney MX API key page](https://ai.eastmoney.com/mxClaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown reports and concise confirmation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes intermediate market-analysis files under /tmp and uploads the final report to an IMA knowledge-base folder when validation passes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
