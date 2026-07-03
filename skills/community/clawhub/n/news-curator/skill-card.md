## Description: <br>
Fetch RSS feeds via curl, curate AI and market news, and deliver scheduled briefings to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hohobohan](https://clawhub.ai/user/hohobohan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or operators use this skill to configure an agent that fetches verified RSS feeds, filters AI and financial market stories, and sends concise scheduled briefings to a Telegram destination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill schedules automatic outbound RSS requests and sends generated briefings to Telegram without a manual approval step. <br>
Mitigation: Review the cron configuration and delivery behavior before enabling scheduled runs. <br>
Risk: The artifact contains a hard-coded Telegram chat destination. <br>
Mitigation: Change the Telegram destination to an approved recipient before installation or execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hohobohan/news-curator) <br>
- [AI News RSS feed](https://artificialintelligence-news.com/feed/) <br>
- [TechCrunch AI RSS feed](https://techcrunch.com/category/artificial-intelligence/feed/) <br>
- [Wired RSS feed](https://www.wired.com/feed/rss) <br>
- [Ars Technica RSS feed](https://arstechnica.com/feed/) <br>
- [MIT Technology Review AI RSS feed](https://www.technologyreview.com/topic/artificial-intelligence/feed/) <br>
- [Benzinga Markets RSS feed](https://www.benzinga.com/markets/feed) <br>
- [Bloomberg Markets RSS feed](https://feeds.bloomberg.com/markets/news.rss) <br>
- [Financial Times Markets RSS feed](https://www.ft.com/markets?format=rss) <br>
- [MarketWatch/Dow Jones RSS feed](https://feeds.content.dowjones.io/public/rss/mw_topstories) <br>
- [Investing.com RSS feed](https://www.investing.com/rss/news.rss) <br>
- [Seeking Alpha market currents feed](https://seekingalpha.com/market_currents.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown briefing with links, notes, and inline shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scheduled cron output is intended for automatic Telegram announcement after RSS retrieval and curation.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
