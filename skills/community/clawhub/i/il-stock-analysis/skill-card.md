## Description:

Comprehensive Israeli stock analysis for TASE-listed securities including fundamental analysis, technical analysis, stock comparisons, and investment report generation with support for Hebrew and English queries, TASE tickers, and ETF numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d14turbo](https://clawhub.ai/user/d14turbo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to analyze TASE-listed stocks and ETFs, compare Israeli securities, and prepare bilingual investment reports. The skill supports fundamental metrics, technical indicators, valuation context, risk assessment, and Buy/Hold/Sell-style recommendations that should be treated as informational analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell helper can expose API credentials when live market-data keys are used.

Mitigation: Prefer the Python fetcher, run helper scripts with a minimal environment, and avoid passing secrets through shell-visible command surfaces.

Risk: Buy/Hold/Sell recommendations and target prices can be mistaken for personal financial advice.

Mitigation: Present recommendations as informational analysis, state assumptions and uncertainty, and require independent review before trading or investment decisions.

Risk: Helper scripts can fall back to template or mock data when live APIs are unavailable.

Mitigation: Label data sources and timestamps clearly, verify whether live API data was returned, and avoid relying on fallback values for investment conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/d14turbo/skills/il-stock-analysis)
- [Financial Metrics for Israeli Stocks](references/financial-metrics.md)
- [Fundamental Analysis for Israeli Stocks](references/fundamental-analysis.md)
- [Report Templates for Israeli Stock Analysis](references/report-template.md)
- [Technical Analysis for Israeli Stocks](references/technical-analysis.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and summaries, with optional JSON market-data output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ILS-denominated tables, source/date notes, Hebrew or English prose, and explicit uncertainty or risk statements.]

## Skill Version(s):

2.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
