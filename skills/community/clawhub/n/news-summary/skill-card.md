## Description: <br>
This skill supports news updates, daily briefings, and current-events requests by fetching trusted international RSS feeds, summarizing key stories, and optionally creating voice summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joargp](https://clawhub.ai/user/joargp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to fetch current public news headlines, summarize 5-8 key stories by topic or region, and optionally produce a short voice briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching current news contacts public RSS providers, and voice generation sends the generated summary text to OpenAI using the user's API key. <br>
Mitigation: Use the skill for public news briefings, avoid including private notes in voice summaries, and confirm that OpenAI API usage and costs are acceptable before generating audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joargp/news-summary) <br>
- [BBC World RSS feed](https://feeds.bbci.co.uk/news/world/rss.xml) <br>
- [BBC News RSS feed](https://feeds.bbci.co.uk/news/rss.xml) <br>
- [Reuters world news feed](https://www.reutersagency.com/feed/?best-regions=world&post_type=best) <br>
- [NPR news RSS feed](https://feeds.npr.org/1001/rss.xml) <br>
- [Al Jazeera RSS feed](https://www.aljazeera.com/xml/rss/all.xml) <br>
- [OpenAI audio speech API](https://api.openai.com/v1/audio/speech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, audio, guidance] <br>
**Output Format:** [Markdown summaries with optional shell commands and generated audio file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text summaries are intended to be concise, typically 5-8 stories; optional voice output uses OpenAI TTS and writes an MP3 file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
