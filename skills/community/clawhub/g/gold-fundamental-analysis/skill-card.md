## Description: <br>
Fetches live gold fundamental data from FRED, CFTC, SPDR/SSGA, Federal Reserve RSS, and ForexFactory/faireconomy.media so an agent can produce bullish, bearish, and neutral factors, a -100 to +100 score, and short-, medium-, and long-term outlooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kimminhpro](https://clawhub.ai/user/kimminhpro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to gather current gold macro, positioning, ETF, Fed, and calendar data and turn it into a structured supplemental XAU/USD fundamental analysis. It is intended for on-demand analysis and scheduled trading-session context, not as standalone financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound live-data requests to FRED, CFTC, SSGA, the Federal Reserve, and faireconomy.media. <br>
Mitigation: Run it only in environments where those network destinations are approved, and review fetched data before relying on the generated analysis. <br>
Risk: The generated analysis could be mistaken for financial advice. <br>
Mitigation: Present the output as supplemental market context and require human review, position sizing, and stop-loss or other risk controls before trading decisions. <br>
Risk: The artifact includes an exposed default FRED API key and accepts FRED credentials by argument or environment variable. <br>
Mitigation: Use a personal FRED_API_KEY or --fred-key value, avoid shared sensitive keys, and remove or rotate the exposed default key before operational use. <br>
Risk: The dependency requirement is broad rather than pinned. <br>
Mitigation: Pin and scan dependencies in the deployment environment before installing the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kimminhpro/gold-fundamental-analysis) <br>
- [FRED API documentation](https://fred.stlouisfed.org/docs/api/fred/) <br>
- [CFTC COT gold data](https://www.cftc.gov/dea/newcot/f_disagg.txt) <br>
- [SPDR Gold Shares](https://www.ssga.com/us/en/intermediary/etfs/spdr-gold-shares-gld) <br>
- [Federal Reserve monetary policy RSS](https://www.federalreserve.gov/feeds/press_monetary.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON data from the Python fetcher followed by a structured Markdown analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires outbound network access to public financial and economic data sources; accepts a FRED API key through --fred-key or FRED_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, created 2026-06-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
