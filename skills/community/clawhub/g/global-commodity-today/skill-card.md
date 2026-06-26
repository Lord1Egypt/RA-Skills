## Description: <br>
Generates concise commodity market briefings for London gold, London silver, LME copper, NYMEX platinum, and Brent crude oil using akshare public market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[M0dZer0](https://clawhub.ai/user/M0dZer0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch recent precious-metals and Brent crude oil prices, then present either a full commodity briefing or a single-commodity status report. The output is informational market data and is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python script and requires installing akshare and pandas. <br>
Mitigation: Review the included script before use and install dependencies only in an environment where local Python execution and public market-data requests are acceptable. <br>
Risk: Commodity prices may be delayed, unavailable during weekends or holidays, or affected by public data-source limitations. <br>
Mitigation: Check the reported data timestamp, retry later when fetches fail, and treat results as informational rather than trading guidance. <br>


## Reference(s): <br>
- [Global Commodity Today on ClawHub](https://clawhub.ai/M0dZer0/global-commodity-today) <br>
- [M0dZer0 ClawHub publisher profile](https://clawhub.ai/user/M0dZer0) <br>
- [AkShare](https://github.com/akfamily/akshare) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown commodity briefing or single-commodity report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include current price, daily change, open, high, low, previous close, data timestamp, failed-fetch notices, and an informational-use disclaimer.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
