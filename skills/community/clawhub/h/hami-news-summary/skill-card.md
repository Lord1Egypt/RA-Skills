## Description:

Fetches and summarizes news from trusted international RSS feeds and can create optional voice summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicenasa](https://clawhub.ai/user/nicenasa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to fetch RSS headlines, summarize current events, group stories by region or topic, and optionally create short voice briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional cloud text-to-speech can send the final news-summary text to OpenAI for speech synthesis.

Mitigation: Use text-only mode for private contexts and request voice generation only when sharing the final summary text with OpenAI is acceptable.

## Reference(s):

- [BBC World News RSS](https://feeds.bbci.co.uk/news/world/rss.xml)
- [BBC Top Stories RSS](https://feeds.bbci.co.uk/news/rss.xml)
- [BBC Business RSS](https://feeds.bbci.co.uk/news/business/rss.xml)
- [BBC Technology RSS](https://feeds.bbci.co.uk/news/technology/rss.xml)
- [Reuters World RSS](https://www.reutersagency.com/feed/?best-regions=world&post_type=best)
- [NPR News RSS](https://feeds.npr.org/1001/rss.xml)
- [Al Jazeera RSS](https://www.aljazeera.com/xml/rss/all.xml)
- [OpenAI Speech API](https://api.openai.com/v1/audio/speech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with optional shell commands for RSS fetching and speech generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text summaries are intended to be concise, typically 5-8 top stories; optional voice output sends the final summary text to OpenAI for speech synthesis.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
