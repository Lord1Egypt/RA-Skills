## Description: <br>
Analyzes recent A-share stock news and events, including news sentiment, institutional validation, and market response, using Investoday financial data to produce structured stock event analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance analysts use this skill to review recent A-share company news, announcements, research sentiment, ratings, and real-time market response for a stock. The output is a structured event analysis report for reference only, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Investoday API key and stock queries may be visible to the data provider. <br>
Mitigation: Use a protected INVESTODAY_API_KEY and avoid submitting confidential watchlists or sensitive query patterns unless the deployment's data-sharing policy allows it. <br>
Risk: Financial news and event analysis can be mistaken for investment advice. <br>
Mitigation: Keep outputs framed as reference analysis, retain the skill's no-investment-advice constraint, and avoid buy, sell, target-price, position-size, or short-term trading recommendations. <br>
Risk: The skill depends on the separate investoday-finance-data helper skill for data access. <br>
Mitigation: Install and review the helper skill before deployment, and confirm its API behavior and credential handling match the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-stock-news-event-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with structured sections and supporting data references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INVESTODAY_API_KEY and the investoday-finance-data helper skill; conclusions are reference analysis and must not include buy, sell, target-price, position-size, or short-term trading advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
