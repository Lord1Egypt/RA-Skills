## Description: <br>
News Crawler fetches news from specified websites or RSS feeds and helps agents generate structured summaries and daily reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Oshin123456](https://clawhub.ai/user/Oshin123456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to retrieve RSS item lists, crawl article pages, and assemble concise news summaries or daily reports from authorized public sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make web requests to user-supplied RSS feeds or article URLs. <br>
Mitigation: Use only public, authorized news sources and avoid localhost, private network addresses, internal services, and sensitive URLs. <br>
Risk: Fetched page content may contain untrusted text. <br>
Mitigation: Treat fetched content as source material for summarization only, not as instructions for the agent to follow. <br>


## Reference(s): <br>
- [RSS News Source Reference](references/rss_sources.md) <br>
- [API Reference](references/api_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Oshin123456/news-crawler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON from helper scripts and Markdown summaries or reports from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [RSS output includes item title, link, description, and published fields; crawl output includes URL, extracted content, and content length.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
