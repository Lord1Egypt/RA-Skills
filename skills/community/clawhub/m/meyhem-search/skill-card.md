## Description: <br>
Web search with LLM-ranked results and freshness control. Queries api.rhdxm.com across multiple engines. No API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c5huracan](https://clawhub.ai/user/c5huracan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Meyhem Search to run web searches, rank results by relevance, apply freshness controls, and optionally fetch page content for a selected result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, agent identifiers, and selected-result URLs are sent to api.rhdxm.com. <br>
Mitigation: Do not use the skill for secrets, private customer information, proprietary research, or sensitive personal data unless the service's privacy and retention terms are acceptable. <br>
Risk: Search results and optional fetched page content may be incomplete, outdated, or misleading. <br>
Mitigation: Review important results before relying on them, especially for security, legal, financial, medical, or operational decisions. <br>


## Reference(s): <br>
- [Meyhem Search on ClawHub](https://clawhub.ai/c5huracan/meyhem-search) <br>
- [Meyhem API documentation](https://api.rhdxm.com/docs) <br>
- [Meyhem MCP endpoint](https://api.rhdxm.com/mcp/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text search results with titles, URLs, relevance scores, snippets, and optional page content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends search queries, agent identifiers, result limits, freshness settings, and selected-result URLs to api.rhdxm.com.] <br>

## Skill Version(s): <br>
0.2.5 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
