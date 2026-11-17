## Description: <br>
RSS新闻订阅免费版 helps agents fetch current headlines and summaries from seven international RSS news sources, with filtering by source, topic, and item limit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to browse lightweight international news updates from public RSS feeds and narrow results by source, topic, or count. It is suited for quick headline and summary retrieval rather than full article extraction, scheduled delivery, or multi-source deduplication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative security verdict is suspicious because the documentation is inconsistent. <br>
Mitigation: Review the skill before installing or running it, and confirm unclear requirements with the publisher. <br>
Risk: The artifact mentions callback URLs and contains inconsistent API-key statements despite server guidance that no malicious behavior was observed. <br>
Mitigation: Do not provide API keys or callback URLs unless the publisher clarifies why they are required. <br>
Risk: Using the skill requires outbound requests to public news RSS sites. <br>
Mitigation: Run it only in environments where external RSS access is acceptable and expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/news-feed-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [BBC News RSS feed](http://feeds.bbci.co.uk/news/rss.xml) <br>
- [Reuters top news RSS feed](https://www.reuters.com/rssFeed/topNews) <br>
- [AP top news RSS feed](https://apnews.com/rss/apf-topnews.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured news summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected summaries include source grouping, title, publication time, short summary, and link; behavior depends on network access to public RSS feeds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
