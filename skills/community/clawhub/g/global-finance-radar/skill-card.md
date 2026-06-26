## Description: <br>
Provides structured global financial analysis across central bank policy, macro indicators, cross-asset markets, valuation, commodities, crypto, fixed income, and risk monitoring using public data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to produce source-aware finance briefs, dashboards, valuation snapshots, and risk matrices for global macro and market questions. It is intended for informational analysis and should disclose data vintage, assumptions, model limits, and non-investment-advice caveats when outputs include forecasts or valuation signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial analyses can be misleading when based on stale, incomplete, or conflicting public market data. <br>
Mitigation: Require source dates, source URLs, data-vintage checks, and cross-validation for key metrics before relying on an output. <br>
Risk: Forecasts, valuation signals, and market commentary may be mistaken for personalized investment, tax, legal, or trading advice. <br>
Mitigation: Present outputs as informational analysis only, disclose assumptions and model limits, and include a non-investment-advice disclaimer for price forecasts or valuation signals. <br>
Risk: Multi-language and cross-region source summaries may omit regulatory context or mistranslate financially material details. <br>
Mitigation: Ask the agent to state covered languages and regions, flag jurisdiction-specific uncertainty, and cite primary sources when available. <br>


## Reference(s): <br>
- [Global Finance Radar on ClawHub](https://clawhub.ai/ai-gaoqian/global-finance-radar) <br>
- [Finance Sources Reference](artifact/references/finance_sources.json) <br>
- [IMF Data](https://www.imf.org/en/Data) <br>
- [World Bank Open Data](https://data.worldbank.org/) <br>
- [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/) <br>
- [ECB Statistical Data Warehouse](https://sdw.ecb.europa.eu/) <br>
- [BIS Statistics](https://www.bis.org/statistics/) <br>
- [OECD Data](https://data.oecd.org/) <br>
- [CoinGecko](https://www.coingecko.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown tables and concise narrative analysis with source dates, assumptions, and risk disclosures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market indicators, valuation signals, forecasts, source URLs, data vintage, and non-investment-advice disclaimers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
