## Description: <br>
Web search using Tavily's LLM-optimized API. Returns relevant results with content snippets, scores, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthew77](https://clawhub.ai/user/matthew77) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily web searches and retrieve LLM-friendly results with snippets, relevance scores, metadata, domain filters, topic filters, and time-range filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and selected search options are sent to Tavily using the user's API key. <br>
Mitigation: Keep the Tavily API key private and avoid submitting secrets, sensitive internal information, or data that should not leave the user's environment. <br>
Risk: Broad searches or raw-content mode can return untrusted or excessive web content. <br>
Mitigation: Use include-domain, exclude-domain, topic, and time-range filters when tighter control is needed, and avoid raw-content mode unless full page content is required. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [ClawHub skill page](https://clawhub.ai/matthew77/liang-tavily-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown search results by default, with pretty-printed JSON available through the --json option.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and TAVILY_API_KEY; supports result count, search depth, topic, time range, domain filters, and optional raw content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
