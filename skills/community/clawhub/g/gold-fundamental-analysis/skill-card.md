## Description:

Fetches gold fundamental data from FRED, CFTC, SPDR ETF, Fed RSS, and economic-calendar sources, then guides an agent to produce bullish and bearish factors, a -100 to +100 score, and short-, medium-, and long-term outlooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kimminhpro](https://clawhub.ai/user/kimminhpro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather gold-market macro, positioning, ETF, Fed-policy, and calendar data for supplementary XAU/USD fundamental analysis. It supports on-demand analysis and scheduled trading-session context, but its output should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound HTTPS requests to public financial-data services, so execution depends on network access and third-party data availability.

Mitigation: Run it in an isolated environment with expected network egress and treat missing or stale data as reduced-confidence analysis.

Risk: The artifact includes an exposed default FRED API key.

Mitigation: Use a controlled FRED_API_KEY environment variable and avoid passing secrets on the command line.

Risk: The output is market analysis support and could be mistaken for investment advice.

Mitigation: Keep the financial-advice disclaimer visible and require users to make independent trading or investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kimminhpro/skills/gold-fundamental-analysis)
- [FRED API documentation](https://fred.stlouisfed.org/docs/api/fred/)
- [CFTC COT disaggregated report](https://www.cftc.gov/dea/newcot/f_disagg.txt)
- [SPDR Gold Shares](https://www.ssga.com/us/en/intermediary/etfs/spdr-gold-shares-gld)
- [Federal Reserve monetary policy RSS feed](https://www.federalreserve.gov/feeds/press_monetary.xml)
- [Source repository referenced by artifact](https://github.com/kimminhpro/gold-fundamental-analysis-skill.git)

## Skill Output:

**Output Type(s):** [json, markdown, guidance]

**Output Format:** [Structured JSON data followed by concise Markdown analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bullish, bearish, and neutral factors; a -100 to +100 fundamental score; short-, medium-, and long-term outlooks; and a confidence estimate.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
