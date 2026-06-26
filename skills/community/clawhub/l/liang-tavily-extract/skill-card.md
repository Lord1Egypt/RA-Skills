## Description: <br>
Extract content from specific URLs using Tavily's extraction API. Returns clean markdown/text from web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthew77](https://clawhub.ai/user/matthew77) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to extract clean markdown, text, or raw JSON from known URLs through Tavily's extraction API, including focused extraction with queries and advanced handling for dynamic pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends submitted URLs, queries, and fetched page content to Tavily's external service. <br>
Mitigation: Use it only for data flows approved by the organization, and avoid private URLs, internal pages, secrets, personal data, or regulated content unless that sharing is authorized. <br>
Risk: The Tavily API key is required for execution and could be exposed if embedded in files or shared logs. <br>
Mitigation: Store the API key in an environment variable or approved secret manager, and do not commit or paste real keys into configuration examples. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Extract API endpoint](https://api.tavily.com/extract) <br>
- [ClawHub release page](https://clawhub.ai/matthew77/liang-tavily-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown, plain text, or JSON printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; accepts up to 20 comma-separated URLs per request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
