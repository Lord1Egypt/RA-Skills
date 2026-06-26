## Description: <br>
Produces structured A-share market broadcast recaps and sentiment commentary from public market breadth, index, and news data supplied by the investoday finance data skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate concise A-share morning, midday, intraday, or after-close market recaps. It helps summarize market breadth, major index performance, hot themes, catalysts, and follow-up signals without presenting the output as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market commentary can become stale quickly or be mistaken for investment advice. <br>
Mitigation: Include the broadcast time and data source, present conclusions as informational commentary, and avoid telling users to buy, sell, or hold securities. <br>
Risk: The skill depends on live public market data supplied by the separate investoday-finance-data skill. <br>
Mitigation: Confirm the dependency is available before generating a recap and clearly state when data is missing, delayed, or outside trading hours. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-stock-market-broadcast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown market recap] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public A-share market data and should remain informational, time-stamped, and non-advisory.] <br>

## Skill Version(s): <br>
1.3.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
