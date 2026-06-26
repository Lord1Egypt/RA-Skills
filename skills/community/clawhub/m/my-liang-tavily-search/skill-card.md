## Description: <br>
Web search using Tavily's LLM-optimized API. Returns relevant results with content snippets, scores, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohMaxy](https://clawhub.ai/user/ohMaxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily web searches and return LLM-oriented answers, source links, snippets, relevance scores, and optional JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and optional raw content requests are sent to Tavily. <br>
Mitigation: Use a dedicated Tavily API key and avoid submitting secrets, private internal URLs, regulated data, or sensitive personal information unless Tavily's data handling is acceptable for the use case. <br>
Risk: Returned web content may be incomplete, stale, misleading, or adversarial. <br>
Mitigation: Treat search results as untrusted reference material and verify important claims against trusted sources before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ohMaxy/my-liang-tavily-search) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown source list by default, or raw JSON when the --json option is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; result count is clamped to 1-20 and optional filters include search depth, topic, time range, domain allowlist, domain blocklist, and raw content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact _meta.json lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
