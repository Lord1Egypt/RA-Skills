## Description: <br>
Search and fetch articles from Grokipedia.com - xAI's AI-generated encyclopedia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirillleventcov](https://clawhub.ai/user/kirillleventcov) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to search Grokipedia and fetch public article content for topic research. It returns structured search results and article text that an agent can cite, summarize, or use as context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and article requests are sent to grokipedia.com. <br>
Mitigation: Use the skill for public lookup topics and avoid sensitive search queries. <br>
Risk: The optional raw HTML output can contain untrusted content. <br>
Mitigation: Treat raw HTML as untrusted and avoid rendering it without sanitization. <br>
Risk: Dependency installation may not be reproducible without a reviewed lockfile. <br>
Mitigation: Use a lockfile or reviewed dependency install process for deployments that require reproducible supply-chain behavior. <br>


## Reference(s): <br>
- [Grokipedia](https://grokipedia.com) <br>
- [Grokipedia Skill Page](https://clawhub.ai/kirillleventcov/grokipedia) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON search results, Markdown article content, optional raw HTML, and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search accepts a query and optional limit from 1 to 50; fetch accepts a case-sensitive article slug and optional raw HTML mode.] <br>

## Skill Version(s): <br>
1.2.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
