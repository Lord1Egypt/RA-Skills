## Description: <br>
This skill supports news updates, daily briefings, and world-event requests by fetching trusted international RSS feeds and optionally creating voice summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niceNASA](https://clawhub.ai/user/niceNASA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to fetch public news RSS feeds, summarize major stories into concise briefings, and optionally create a voice version of the summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches current headlines from public RSS feeds, so summaries may reflect incomplete, changing, or source-specific reporting. <br>
Mitigation: Review important summaries against cited sources and use multiple listed feeds when balance or accuracy matters. <br>
Risk: Optional voice generation sends the generated summary text to OpenAI and uses an OpenAI API key, which may incur usage costs. <br>
Mitigation: Use voice summaries only for non-sensitive summary text and only when the operator is comfortable with the API call and associated billing. <br>


## Reference(s): <br>
- [BBC World News RSS](https://feeds.bbci.co.uk/news/world/rss.xml) <br>
- [BBC Top Stories RSS](https://feeds.bbci.co.uk/news/rss.xml) <br>
- [BBC Business RSS](https://feeds.bbci.co.uk/news/business/rss.xml) <br>
- [BBC Technology RSS](https://feeds.bbci.co.uk/news/technology/rss.xml) <br>
- [Reuters World Feed](https://www.reutersagency.com/feed/?best-regions=world&post_type=best) <br>
- [NPR News RSS](https://feeds.npr.org/1001/rss.xml) <br>
- [Al Jazeera RSS](https://www.aljazeera.com/xml/rss/all.xml) <br>
- [OpenAI Audio Speech API](https://api.openai.com/v1/audio/speech) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Audio file] <br>
**Output Format:** [Markdown news summary with optional shell commands and optional MP3 audio output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are intended to be concise, typically 5-8 top stories and about two minutes maximum for voice output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
