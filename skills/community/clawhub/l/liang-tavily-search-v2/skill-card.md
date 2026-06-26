## Description: <br>
Web search using Tavily's LLM-optimized API. Returns relevant results with content snippets, scores, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15914355527](https://clawhub.ai/user/15914355527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily web searches from a Node.js command-line script and receive LLM-oriented answer text, source snippets, relevance scores, metadata, or raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, domain filters, time ranges, and similar options are sent to Tavily under the configured API key. <br>
Mitigation: Avoid submitting secrets or sensitive internal data, and use a dedicated Tavily API key where possible. <br>
Risk: Returned web results may be incomplete, stale, or unsuitable for high-stakes decisions without review. <br>
Mitigation: Verify important claims against the returned source URLs and use domain or time filters when precision or recency matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/15914355527/liang-tavily-search-v2) <br>
- [Publisher Profile](https://clawhub.ai/user/15914355527) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Search API Endpoint](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown summaries by default, or raw JSON when --json is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; supports result count, depth, topic, time range, domain filters, raw content, and JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
