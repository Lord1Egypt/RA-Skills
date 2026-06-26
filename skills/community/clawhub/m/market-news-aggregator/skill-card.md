## Description: <br>
Aggregate, classify, summarize, and analyze market news from Chinese financial portals (Sina Finance, EastMoney, Hexun, Jin10). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Market analysts, traders, and financial-news reviewers use this skill to collect Chinese market news, identify sector relevance, summarize key items, tag sentiment, and rank market-moving importance across pre-market, intraday, and end-of-day workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial-news summaries may be mistaken for investment advice or forward-looking recommendations. <br>
Mitigation: Present outputs as news analysis, retain source attribution, and require user review before making trading or investment decisions. <br>
Risk: Repeated automated fetching of financial-news sites can create unnecessary load or violate site expectations. <br>
Mitigation: Use moderate intervals, one fetch per source per scenario, reasonable character limits, and respect robots.txt as described in the artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/market-news-aggregator) <br>
- [Sina Finance](https://finance.sina.com.cn/) <br>
- [EastMoney](https://www.eastmoney.com/) <br>
- [Hexun](https://www.hexun.com/) <br>
- [Jin10](https://www.jin10.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown market briefing with ranked news items, source attribution, summaries, keywords, sentiment tags, and sector rollups; may include example shell commands for optional batch fetching.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses moderate public-web fetches with source attribution; does not request credentials or persistent access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
