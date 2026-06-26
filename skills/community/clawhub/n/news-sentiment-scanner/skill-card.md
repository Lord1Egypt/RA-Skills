## Description: <br>
Scan news sources and RSS feeds for events that could move prediction market prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and prediction-market users use this skill to scan current headlines, score market impact, flag urgent stories, and cross-reference news with active markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News-driven market signals can be stale, incomplete, or misleading if a feed is delayed or a headline lacks context. <br>
Mitigation: Ask the agent to list the exact feeds and links it used, then verify urgent claims independently before trading or acting on them. <br>
Risk: The skill makes outbound requests to public news and RSS feeds. <br>
Mitigation: Use it only in environments where outbound access to public feeds is acceptable, and review any substituted feeds before relying on their results. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/rsquaredsolutions2026/news-sentiment-scanner) <br>
- [AgentBets tutorial](https://agentbets.ai/guides/openclaw-news-sentiment-scanner-skill/) <br>
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>
- [AP Top News RSS feed](https://feeds.apnews.com/rss/apf-topnews) <br>
- [Reuters Top News RSS feed](https://feeds.reuters.com/reuters/topNews) <br>
- [ESPN News RSS feed](https://www.espn.com/espn/rss/news) <br>
- [Cointelegraph RSS feed](https://cointelegraph.com/rss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with headline summaries, sentiment notes, source links, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include urgency flags, market-impact scores, source attribution, and suggested verification steps.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
