## Description:

This skill supports news updates, daily briefings, and world-event queries by fetching trusted international RSS feeds and creating optional voice summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joargp](https://clawhub.ai/user/joargp)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to fetch current RSS headlines from international news sources and turn them into concise text or optional voice briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional voice summaries send the summary text to OpenAI TTS.

Mitigation: Use voice mode only when sending the summary content to OpenAI is acceptable.

Risk: The example writes audio to a fixed /tmp/news.mp3 path.

Mitigation: Use a unique, private temporary filename for operational use.

## Reference(s):

- [BBC World News RSS](https://feeds.bbci.co.uk/news/world/rss.xml)
- [BBC Top Stories RSS](https://feeds.bbci.co.uk/news/rss.xml)
- [BBC Business RSS](https://feeds.bbci.co.uk/news/business/rss.xml)
- [BBC Technology RSS](https://feeds.bbci.co.uk/news/technology/rss.xml)
- [Reuters World Feed](https://www.reutersagency.com/feed/?best-regions=world&post_type=best)
- [NPR News RSS](https://feeds.npr.org/1001/rss.xml)
- [Al Jazeera RSS](https://www.aljazeera.com/xml/rss/all.xml)
- [OpenAI Audio Speech API](https://api.openai.com/v1/audio/speech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown news briefing with optional shell commands and voice-summary audio output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional voice summaries may produce an MP3 audio file.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
