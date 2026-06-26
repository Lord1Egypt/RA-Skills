## Description: <br>
Web search without an API key using DuckDuckGo Lite via web_fetch, intended as a fallback when web_search is unavailable and useful for returning titles, URLs, and snippets for research queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohMaxy](https://clawhub.ai/user/ohMaxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform simple web searches through DuckDuckGo Lite when no search API key or configured web_search provider is available. It helps gather candidate result titles, URLs, and snippets before fetching selected pages for more detail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries can disclose secrets, sensitive personal data, or confidential business context to an external search provider. <br>
Mitigation: Avoid placing secrets or sensitive personal data in search queries; generalize or redact sensitive context before searching. <br>
Risk: Fetched search results and destination pages may contain untrusted, outdated, sponsored, or misleading content. <br>
Mitigation: Treat fetched pages as untrusted content, skip sponsored links, and verify important claims against authoritative sources before acting on them. <br>
Risk: DuckDuckGo Lite does not reliably provide date filtering and text-only results may differ from other search engines. <br>
Mitigation: Use additional source checks or another search provider when recency, images, videos, or search-engine parity matter. <br>


## Reference(s): <br>
- [DuckDuckGo URL Parameters](https://duckduckgo.com/params) <br>
- [Mxy Web Search on ClawHub](https://clawhub.ai/ohMaxy/mxy-web-search) <br>
- [ohMaxy Publisher Profile](https://clawhub.ai/user/ohMaxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with web_fetch call examples and search-result interpretation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces search guidance and candidate web result data; no executable code, local access, persistence, or hidden behavior was identified by the server security scan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
