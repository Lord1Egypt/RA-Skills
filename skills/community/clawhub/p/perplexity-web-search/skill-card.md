## Description: <br>
Web search and URL fetching via Perplexity, with default Sonar search, optional Sonar Pro depth, and local URL content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aligurelli](https://clawhub.ai/user/aligurelli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to let an agent search the web with Perplexity, fetch URL content as markdown or text, and configure Perplexity-backed web search settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Perplexity's API and may include sensitive data if users enter secrets or private URLs. <br>
Mitigation: Use a dedicated Perplexity API key where possible and avoid sending secrets, credentials, private URLs, or confidential content in search queries. <br>
Risk: Perplexity data handling and account terms govern API usage for this skill. <br>
Mitigation: Review Perplexity's data handling expectations and account terms before using the skill with sensitive or regulated information. <br>
Risk: Optional deeper Perplexity models can increase cost. <br>
Mitigation: Use the default Sonar model for routine searches and enable Sonar Pro or reasoning models only when deeper analysis is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aligurelli/perplexity-web-search) <br>
- [Perplexity API endpoint](https://api.perplexity.ai) <br>
- [Perplexity API key settings](https://www.perplexity.ai/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text answers with citations, fetched page content, and JSON5 configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results depend on the configured Perplexity model and query parameters such as count, country, language, and freshness.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
