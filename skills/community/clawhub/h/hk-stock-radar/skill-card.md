## Description: <br>
Hk Stock Radar helps agents monitor Hong Kong stock indices, individual quotes, sector moves, southbound capital flow, and related news or social sentiment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gold3bear](https://clawhub.ai/user/gold3bear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and agents use this skill to check Hong Kong market direction, quote major stocks, compare sector moves, and summarize live market signals before forming a market readout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger external market and news requests, so outputs may depend on third-party availability, freshness, and data quality. <br>
Mitigation: Confirm important market conclusions against authoritative market data before acting on them. <br>
Risk: The skill text proposes using a logged-in X/Twitter browser session for sentiment searches, which may expose account-context activity without clear consent boundaries. <br>
Mitigation: Use unauthenticated or read-only, user-approved browsing for social sentiment checks unless the user explicitly authorizes account-context searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gold3bear/hk-stock-radar) <br>
- [Publisher profile](https://clawhub.ai/user/gold3bear) <br>
- [Sina Finance Hong Kong quote endpoint](https://hq.sinajs.cn/list=hkHSI,hkHSTECH,hkHSCEI) <br>
- [Eastmoney Hong Kong sector endpoint](http://push2.eastmoney.com/api/qt/clist/get) <br>
- [Google News RSS Hong Kong market search](https://news.google.com/rss/search?q=%E6%B8%AF%E8%82%A1+%E6%81%92%E7%94%9F+%E4%BB%8A%E6%97%A5+when:1h) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with market-data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live market values from third-party financial and news sources.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
