## Description: <br>
Market Analyst helps agents analyze global assets, including Vietnam and US stocks, forex, gold, oil, crypto, ETFs, DCA plans, and portfolios, using technical indicators, valuation metrics, and bundled market-scanning scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddieluong](https://clawhub.ai/user/eddieluong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research market conditions, screen assets, compare asset classes, estimate returns, and draft portfolio or DCA guidance. It is intended for educational investment analysis and should not be treated as personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled Python scripts can send requested tickers or portfolio symbols to external market-data services. <br>
Mitigation: Run the scripts only when the user accepts external data lookups, and avoid sending sensitive portfolio details when privacy is a concern. <br>
Risk: Market recommendations and macro assumptions can become stale or misleading. <br>
Mitigation: Verify current prices, data sources, macro context, and assumptions before acting on any output. <br>
Risk: Users may over-rely on educational analysis as personalized financial advice. <br>
Mitigation: Present results as research, preserve investment-advice disclaimers, and encourage independent review or qualified professional advice for personal decisions. <br>


## Reference(s): <br>
- [Advanced Technical Analysis](references/advanced-ta.md) <br>
- [Crypto & BNB Analysis Framework](references/crypto-analysis.md) <br>
- [Financial Analysis Knowledge Base](references/financial-analysis-knowledge.md) <br>
- [Forex Guide](references/forex-guide.md) <br>
- [Global ETF Guide](references/global-etf.md) <br>
- [Gold / XAUUSD Analysis Framework](references/gold-analysis.md) <br>
- [Macro Update - March 2026](references/macro-update-2026-03.md) <br>
- [Return Estimation](references/return-estimation.md) <br>
- [Sector Fundamentals - Vietnam Stock Market](references/sector-fundamentals.md) <br>
- [Sector Fundamentals Update - Q1 2026](references/sector-update-2026.md) <br>
- [VN Stock Swing Trading & Scalping](references/swing-trading-vn.md) <br>
- [US Equities Analysis Guide](references/us-equities.md) <br>
- [ClawHub skill page](https://clawhub.ai/eddieluong/market-analyst) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with tables, bullet points, and inline shell or Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ticker-specific analysis, portfolio allocations, DCA plans, and scenario estimates; outputs are educational research and require user verification.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
