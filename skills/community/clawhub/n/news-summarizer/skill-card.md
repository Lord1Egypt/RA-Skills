## Description:

Fetch and summarize world news from BBC, Reuters, NPR RSS feeds, with optional voice summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to get concise daily or current-event briefings from major RSS news sources, grouped by region or topic. It can also create an audio version of the generated briefing when text-to-speech is appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional voice summaries send the generated news summary to OpenAI text-to-speech.

Mitigation: Use text-only mode for sensitive briefings or content that should not be sent to an external speech service.

Risk: The documented audio command writes output to /tmp/news.mp3, which may be visible on shared systems.

Mitigation: Choose a private temporary path or remove the generated audio file after use on shared machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/news-summarizer)
- [BBC World RSS feed](https://feeds.bbci.co.uk/news/world/rss.xml)
- [Reuters world news feed](https://www.reutersagency.com/feed/?best-regions=world&post_type=best)
- [NPR News RSS feed](https://feeds.npr.org/1001/rss.xml)
- [The Hindu national news RSS feed](https://www.thehindu.com/news/national/feeder/default.rss)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown briefing text with optional audio generation command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional voice mode sends the generated news summary to OpenAI text-to-speech and may write audio to /tmp/news.mp3.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
