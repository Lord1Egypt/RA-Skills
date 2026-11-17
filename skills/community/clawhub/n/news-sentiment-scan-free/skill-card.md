## Description: <br>
Scans Hong Kong, US, and A-share company announcements and financial news, removes noise, scores sentiment from -10 to +10, and produces a basic sentiment thermometer with a major-events list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, individual investors, and research analysts use this skill to run short-term public-news sentiment scans for a single stock across Hong Kong, US, or A-share markets. It helps summarize recent news direction and event drivers, but it is not a substitute for investment advice or independent financial analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow fetches financial news and market data from external sources. <br>
Mitigation: Use it only in environments where external market/news data access is acceptable, and review the selected sources before relying on the report. <br>
Risk: A callback URL could send results outside the local agent session. <br>
Mitigation: Provide a callback URL only when external delivery is intentional and the destination is trusted. <br>
Risk: Sentiment scores can be incomplete or misleading, especially for sparse coverage, sarcasm, metaphor, or fast-moving financial events. <br>
Mitigation: Treat the report as a screening aid, verify major events against original sources, and avoid using it as investment advice. <br>
Risk: The skill includes command execution guidance with loose script placeholders. <br>
Mitigation: Confirm the exact command, ticker, market, time window, and local script path before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/news-sentiment-scan-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Yahoo Finance](https://finance.yahoo.com/) <br>
- [Google News](https://news.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain-text sentiment report with a score thermometer, major-event list, source notes, statistics, and suggested follow-up checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock ticker, monitoring window, market selection, sentiment score, confidence, source, and event timestamp fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
