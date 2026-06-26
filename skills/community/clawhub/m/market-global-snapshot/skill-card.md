## Description: <br>
Generate a structured global market snapshot report including major stock indices and commodities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiediking](https://clawhub.ai/user/jiediking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce current global market summaries for major U.S., China, Japan, and India stock indices plus selected commodities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated market prices may be delayed, unavailable, or parsed incorrectly from public finance websites. <br>
Mitigation: Treat outputs as informational and verify important financial decisions independently against authoritative market data sources. <br>
Risk: The skill makes web requests to public finance sites to retrieve current market data. <br>
Mitigation: Install only where outbound web access to those public finance sites is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiediking/market-global-snapshot) <br>
- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?interval=1d&range=5d) <br>
- [Trading Economics United States stock market](https://tradingeconomics.com/united-states/stock-market) <br>
- [Trading Economics China stock market](https://tradingeconomics.com/china/stock-market) <br>
- [Trading Economics Japan stock market](https://tradingeconomics.com/japan/stock-market) <br>
- [Trading Economics India stock market](https://tradingeconomics.com/india/stock-market) <br>
- [Sina Finance quote endpoint](https://hq.sinajs.cn/list=sh000680) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown market snapshot with timestamped prices, changes, percentages, and availability notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public market data and returns partial results with N/A markers when sources fail.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
