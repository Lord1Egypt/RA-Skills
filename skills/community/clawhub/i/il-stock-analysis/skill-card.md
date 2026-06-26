## Description: <br>
Comprehensive Israeli stock analysis for TASE-listed securities including fundamental analysis, technical analysis, stock comparisons, and investment report generation with support for Hebrew and English queries, TASE tickers, company names, and ETF numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d14turbo](https://clawhub.ai/user/d14turbo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to analyze Israeli stocks and ETFs traded on TASE, including quick stock summaries, fundamental and technical analysis, peer comparisons, and formatted investment reports. It is intended for market-analysis assistance and should not replace independent investment review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may query external financial-data providers for requested Israeli securities. <br>
Mitigation: Configure only intended API keys and avoid sharing private portfolio, account, or sensitive trading details unless necessary. <br>
Risk: The skill can generate investment-style opinions that may be incomplete, stale, or incorrect. <br>
Mitigation: Independently verify data, assumptions, recommendations, and risk factors before making any investment decision. <br>
Risk: Bundled fetch scripts can fall back to template or mock data when live APIs are unavailable. <br>
Mitigation: Check the reported source and timestamp, and confirm live data access before relying on generated market analysis. <br>


## Reference(s): <br>
- [Financial Metrics for Israeli Stocks](references/financial-metrics.md) <br>
- [Fundamental Analysis for Israeli Stocks](references/fundamental-analysis.md) <br>
- [Report Templates for Israeli Stock Analysis](references/report-template.md) <br>
- [Technical Analysis for Israeli Stocks](references/technical-analysis.md) <br>
- [ClawHub skill page](https://clawhub.ai/d14turbo/il-stock-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with tables, recommendations, risk summaries, and optional JSON from bundled data-fetch scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ILS-denominated market data, source dates, Hebrew or English terminology, and explicit uncertainty notes.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
