## Description:

Free local web search via DuckDuckGo HTML scraping with no API key, source trust scoring, retry/backoff handling, and JSON output suitable for pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mes28io](https://clawhub.ai/user/mes28io)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run web searches when a hosted web_search tool is unavailable or lacks credentials. It returns ranked DuckDuckGo HTML search results with snippets, source URLs, a trust score, and safety disclaimers for follow-up verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to DuckDuckGo through HTML scraping.

Mitigation: Use only non-secret, non-sensitive queries and avoid entering credentials, private customer data, or confidential project details.

Risk: DuckDuckGo HTML selectors or endpoint behavior may change, causing missing or malformed results.

Mitigation: Treat empty or unexpected output as a parser compatibility issue and verify important searches through another source before relying on them.

Risk: Trust scores are heuristic and search snippets can be incomplete or misleading.

Mitigation: Use trust scores for filtering only and confirm important claims directly with primary sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mes28io/skills/local-web-search-skill)
- [DuckDuckGo HTML search endpoint](https://duckduckgo.com/html/?q=)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON object printed to stdout, with query, count, disclaimer, security note, and results containing title, URL, snippet, and trust metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on DuckDuckGo HTML availability and parser compatibility; trust scores are ranking aids and do not replace primary-source verification.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
