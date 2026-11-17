## Description:

Fetch and summarize global news from BBC, Reuters, NPR, and The Hindu RSS feeds into concise text or optional voice briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch public RSS headlines from major news sources, summarize current events into a concise briefing, and optionally create an audio version of the summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice summaries require sending generated summary text to OpenAI and creating /tmp/news.mp3 locally.

Mitigation: Use the text-only workflow for sensitive or proprietary prompts, and delete /tmp/news.mp3 if the audio file should not remain on disk.

Risk: News summaries may reflect stale, incomplete, or source-specific RSS feed coverage.

Mitigation: Fetch feeds at use time, keep summaries concise, balance coverage across the configured sources, and cite source feeds when requested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/news-summarizer-official)
- [BBC World News RSS](https://feeds.bbci.co.uk/news/world/rss.xml)
- [Reuters Agency World Feed](https://www.reutersagency.com/feed/?best-regions=world&post_type=best)
- [NPR News RSS](https://feeds.npr.org/1001/rss.xml)
- [The Hindu National News RSS](https://www.thehindu.com/news/national/feeder/default.rss)
- [OpenAI Audio Speech API](https://api.openai.com/v1/audio/speech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown news briefing with optional shell commands for RSS fetching and audio generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional voice workflow sends generated summary text to OpenAI TTS and writes /tmp/news.mp3 locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
