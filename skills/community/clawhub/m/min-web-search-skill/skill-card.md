## Description:

Minimal cross-platform web search via Bing RSS - no API key, no dependencies beyond Python 3.8+ or curl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cute-omega](https://clawhub.ai/user/cute-omega)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform basic web searches when a built-in web search tool is unavailable, unreachable, or not configured. It returns search result titles, URLs, and snippets from Bing RSS in human-readable or JSON form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Bing through the public RSS endpoint.

Mitigation: Avoid searching for secrets, credentials, private customer data, or confidential internal terms.

Risk: Search results depend on external network availability and Bing RSS behavior.

Mitigation: Treat results as retrieved web evidence, check source quality before relying on them, and handle empty or failed searches gracefully.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cute-omega/skills/min-web-search-skill)
- [Publisher profile](https://clawhub.ai/user/cute-omega)
- [Bing RSS search endpoint](https://www.bing.com/search?q={query}&format=rss)

## Skill Output:

**Output Type(s):** [text, json, shell commands, code, guidance]

**Output Format:** [Human-readable search results or JSON objects with title, URL, and snippet fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a small single-query result set; the RSS endpoint may return about 10 results and no pagination.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
