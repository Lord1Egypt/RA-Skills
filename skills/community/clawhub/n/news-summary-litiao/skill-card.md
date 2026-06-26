## Description: <br>
This skill should be used when the user asks for news updates, daily briefings, or what's happening in the world. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and agents use this skill to fetch current news from international RSS feeds, summarize the main stories, and optionally create a short voice briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice mode sends generated summary text to OpenAI for text-to-speech and writes a temporary audio file. <br>
Mitigation: Use voice output only when the summary text is appropriate to send to OpenAI, and handle the temporary audio file according to local data-retention expectations. <br>
Risk: Bundled metadata differs from the registry listing. <br>
Mitigation: Confirm the package identity and registry listing before installing or deploying the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/news-summary-litiao) <br>
- [BBC World News RSS](https://feeds.bbci.co.uk/news/world/rss.xml) <br>
- [Reuters World Feed](https://www.reutersagency.com/feed/?best-regions=world&post_type=best) <br>
- [NPR News RSS](https://feeds.npr.org/1001/rss.xml) <br>
- [Al Jazeera RSS](https://www.aljazeera.com/xml/rss/all.xml) <br>
- [OpenAI Audio Speech API](https://api.openai.com/v1/audio/speech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown news summary with optional bash commands and audio-generation API call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are intended to stay concise, usually 5-8 top stories or about a two-minute voice briefing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
