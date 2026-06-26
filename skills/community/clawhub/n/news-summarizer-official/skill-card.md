## Description: <br>
Fetch and summarize global news from BBC, Reuters, NPR RSS feeds into concise text or voice briefings covering major current events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch current headlines from RSS feeds, summarize major stories, and optionally create a short voice briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News keywords, fetched article text, summaries, and generated scripts may be sent to configured search, model, image, or text-to-speech providers. <br>
Mitigation: Use local providers where possible for sensitive topics, remove cloud API keys when they are not needed, and review provider fallback behavior when strict routing matters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/terrycarter1985/news-summarizer-official) <br>
- [BBC World RSS feed](https://feeds.bbci.co.uk/news/world/rss.xml) <br>
- [BBC Top Stories RSS feed](https://feeds.bbci.co.uk/news/rss.xml) <br>
- [Reuters world feed](https://www.reutersagency.com/feed/?best-regions=world&post_type=best) <br>
- [NPR News RSS feed](https://feeds.npr.org/1001/rss.xml) <br>
- [The Hindu national news RSS feed](https://www.thehindu.com/news/national/feeder/default.rss) <br>
- [OpenAI audio speech API](https://api.openai.com/v1/audio/speech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands for RSS fetching and voice generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate concise text briefings or an MP3 voice summary when configured with a text-to-speech provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
