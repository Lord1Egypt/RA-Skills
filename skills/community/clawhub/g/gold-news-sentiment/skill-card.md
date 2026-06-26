## Description: <br>
Use this skill when users want to pull recent global gold-related news, assess short-term or medium-term market sentiment for gold, connect macro drivers like Fed policy, US yields, USD, inflation, geopolitics, and ETF flows to gold, and produce a structured conclusion such as 看涨, 看跌, or 观望 with confidence and risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyecho-io](https://clawhub.ai/user/cyecho-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to refresh recent gold-related news, deduplicate weak or repeated signals, and produce a structured gold sentiment report with short-term and medium-term direction, confidence, drivers, news links, and risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled Python scripts query public Google and Bing News endpoints and write local cache files for faster future sentiment reports. <br>
Mitigation: Run refreshes only when news retrieval is needed, review the configured schedule for recurring updates, and inspect generated cache files before relying on them. <br>
Risk: Gold sentiment output may be mistaken for financial advice or a trading recommendation. <br>
Mitigation: Treat reports as market analysis support, preserve uncertainty and invalidation notes, and require independent review before investment decisions. <br>
Risk: A partial or failed news retrieval can make the evidence base too thin for a reliable conclusion. <br>
Mitigation: Do not fabricate a sentiment call when retrieval fails; report insufficient evidence or rerun with a narrower query. <br>


## Reference(s): <br>
- [Gold News Sentiment ClawHub Release](https://clawhub.ai/cyecho-io/gold-news-sentiment) <br>
- [Automation Template](references/automation-template.md) <br>
- [Scoring Rules](references/scoring-rules.md) <br>
- [Source List](references/source-list.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown sentiment report with optional JSON news snapshots and local cache files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should include explicit timeframe, bullish and bearish evidence, confidence, core drivers, relevant links, uncertainty, and invalidation risks.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
