## Description: <br>
News Summary Voice helps an agent fetch public RSS news sources, summarize current events, and optionally prepare voice briefing commands across macOS, Linux, and Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realorange1994](https://clawhub.ai/user/realorange1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to assemble multilingual daily news briefings from selected public RSS sources. It supports text summaries and optional voice playback or TTS-oriented commands for routine news updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RSS sources can be unavailable, stale, restricted by region, or different from the user's trusted news sources. <br>
Mitigation: Verify the feed list before relying on a briefing and prefer sources the user has explicitly requested or approved. <br>
Risk: Voice generation or external TTS services may expose sensitive or private text if used with confidential content. <br>
Mitigation: Avoid sending sensitive text to external TTS services and use local speech tools when privacy requirements apply. <br>
Risk: Scheduled news briefings can run unexpectedly if enabled outside the skill. <br>
Mitigation: Enable scheduled execution only through an explicit scheduler that the user can review, pause, and disable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realorange1994/news-summary-voice) <br>
- [BBC World RSS feed](https://feeds.bbci.co.uk/news/world/rss.xml) <br>
- [Reuters World News feed](https://www.reutersagency.com/feed/?best-topics=world-news) <br>
- [NPR News RSS feed](https://feeds.npr.org/1001/rss.xml) <br>
- [Hacker News RSS feed](https://news.ycombinator.com/rss) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown briefing with links, summaries, source attribution, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optional voice playback or TTS generation steps depending on the user's platform and request.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
