## Description: <br>
Analyzes recent A-share stock news, company announcements, institutional sentiment, and market reaction using Investoday financial data, then produces a structured event-analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External finance users and agents use this skill to interpret recent A-share company news, announcements, research sentiment, ratings, and real-time market feedback. The skill produces informational event analysis and explicitly avoids trading, target-price, position-sizing, or short-term operation advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may activate the skill for loosely related stock-news requests. <br>
Mitigation: Review and narrow trigger phrases if tighter activation is needed. <br>
Risk: The skill uses network and current-data lookups for market-news interpretation. <br>
Mitigation: Install only when that behavior is desired and verify that the dependent investoday-finance-data skill is available and trusted. <br>
Risk: Market analysis may be mistaken for trading advice. <br>
Mitigation: Keep outputs informational and preserve the artifact's prohibition on buy or sell advice, target-price projections, position sizing, and short-term operation recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-stock-message-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown stock-news event analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public-market data lookups through the required investoday-finance-data skill and frames conclusions as informational analysis, not investment advice.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
