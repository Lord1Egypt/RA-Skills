## Description: <br>
Search the web using Perplexity's Search API for ranked, real-time web results with advanced filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[M4vF14](https://clawhub.ai/user/M4vF14) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to let an agent run current web searches through Perplexity, with optional result-count and recency controls for research, news lookup, market research, and competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Perplexity and may include sensitive information if users include it in prompts. <br>
Mitigation: Avoid secrets, regulated personal data, and confidential business details in search queries. <br>
Risk: Perplexity API requests can consume paid quota under the user's own API key. <br>
Mitigation: Monitor Perplexity account usage and configure access only for users who should spend that quota. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/M4vF14/perplexity-search-skill) <br>
- [Perplexity API documentation](https://docs.perplexity.ai) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Perplexity API account and usage](https://perplexity.ai/account/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Formatted text or JSON search results with titles, URLs, snippets, and optional dates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PERPLEXITY_API_KEY; supports result count from 1 to 10 and optional day, week, month, or year recency filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json, and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
