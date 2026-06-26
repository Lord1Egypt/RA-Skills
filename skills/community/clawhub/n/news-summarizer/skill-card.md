## Description: <br>
Fetches and summarizes world news from BBC, Reuters, NPR, and related RSS feeds, with optional voice summary generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch current public-news RSS items, summarize the most important stories, and optionally prepare a short voice briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional voice summaries send generated summary text to OpenAI text-to-speech and require an OpenAI API key. <br>
Mitigation: Use voice summaries only when the user accepts that transfer, avoid private or sensitive context in voiced summaries, and protect the API key as a sensitive credential. <br>
Risk: News summaries are generated from public RSS feeds and may omit context, updates, or alternative perspectives. <br>
Mitigation: Cite and review the source feeds for high-impact or time-sensitive news before relying on the summary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/news-summarizer) <br>
- [BBC World RSS Feed](https://feeds.bbci.co.uk/news/world/rss.xml) <br>
- [BBC Top Stories RSS Feed](https://feeds.bbci.co.uk/news/rss.xml) <br>
- [Reuters Agency World Feed](https://www.reutersagency.com/feed/?best-regions=world&post_type=best) <br>
- [NPR News RSS Feed](https://feeds.npr.org/1001/rss.xml) <br>
- [The Hindu National News RSS Feed](https://www.thehindu.com/news/national/feeder/default.rss) <br>
- [OpenAI Audio Speech API](https://api.openai.com/v1/audio/speech) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with optional inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional voice workflow can produce an MP3 audio briefing using OpenAI text-to-speech.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
