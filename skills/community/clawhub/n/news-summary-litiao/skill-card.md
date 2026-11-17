## Description:

This skill should be used when the user asks for news updates, daily briefings, or what's happening in the world. Fetches news from trusted international RSS feeds and can create voice summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect current public headlines from international RSS feeds, produce concise news briefings, and optionally generate a voice briefing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice summaries send generated briefing text to OpenAI for speech generation.

Mitigation: Avoid including private notes or sensitive user context in a voice briefing unless that data transfer is intended.

Risk: News summaries are based on public RSS feeds and may reflect source coverage gaps or breaking-news changes.

Mitigation: Use multiple listed feeds for important briefings and cite sources when requested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/news-summary-litiao)
- [BBC World News RSS](https://feeds.bbci.co.uk/news/world/rss.xml)
- [Reuters World Feed](https://www.reutersagency.com/feed/?best-regions=world&post_type=best)
- [NPR News RSS](https://feeds.npr.org/1001/rss.xml)
- [Al Jazeera RSS](https://www.aljazeera.com/xml/rss/all.xml)
- [OpenAI Audio Speech API endpoint](https://api.openai.com/v1/audio/speech)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Concise Markdown news briefing with optional shell commands and MP3 audio output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice summaries require OPENAI_API_KEY and send generated briefing text to OpenAI for speech generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
