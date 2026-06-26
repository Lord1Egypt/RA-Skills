## Description: <br>
Free local web search via DuckDuckGo HTML scraping with no API key for fast query results with source trust scoring, retry/backoff handling, and JSON output suitable for pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mes28io](https://clawhub.ai/user/mes28io) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run local web searches when a hosted web search tool is unavailable or lacks credentials. It returns search results with snippets, URLs, security/disclaimer text, and trust scores to support follow-up verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search query text is sent to DuckDuckGo. <br>
Mitigation: Do not include secrets, credentials, private customer data, or confidential business details in search queries. <br>
Risk: Returned snippets and trust scores may be incomplete, stale, or misleading. <br>
Mitigation: Treat search results as untrusted web content and verify important claims from primary sources before acting on them. <br>
Risk: Public DuckDuckGo HTML behavior can change, which may break parsing or reduce result quality. <br>
Mitigation: Check output count, errors, and result structure during use; update the parser when endpoint markup changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mes28io/local-web-search-skill) <br>
- [DuckDuckGo HTML search endpoint](https://duckduckgo.com/html/?q=) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON search results with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes query, count, disclaimer, security note, result title, URL, snippet, and trust score metadata; results depend on public DuckDuckGo HTML behavior.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
