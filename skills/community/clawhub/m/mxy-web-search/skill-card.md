## Description:

Web search without an API key using DuckDuckGo Lite via web_fetch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohmaxy](https://clawhub.ai/user/ohmaxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run text web searches through DuckDuckGo Lite when no dedicated search API key is configured, then select result URLs for follow-up reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to DuckDuckGo Lite and selected result pages may be fetched afterward.

Mitigation: Avoid submitting sensitive or confidential queries unless that external network use is acceptable.

Risk: Search results and snippets can be incomplete, sponsored, stale, or misleading.

Mitigation: Skip sponsored entries and verify important claims by fetching and reviewing authoritative result pages.

## Reference(s):

- [Mxy Web Search on ClawHub](https://clawhub.ai/ohmaxy/skills/mxy-web-search)
- [DuckDuckGo Parameters](https://duckduckgo.com/params)
- [DuckDuckGo Lite Search Endpoint](https://lite.duckduckgo.com/lite/?q=QUERY)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown guidance with web_fetch URL examples and text search result interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns titles, URLs, and snippets from DuckDuckGo Lite; supports regional filtering with the kl query parameter.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
