## Description:

Search the web using a self-hosted SearXNG metasearch engine. Aggregates Google, Brave, DuckDuckGo, and more without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stperic](https://clawhub.ai/user/stperic)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to retrieve current web search results through a trusted SearXNG instance without configuring commercial search API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the configured SearXNG server and may expose sensitive or personal information, especially when HTTP is used.

Mitigation: Use only a trusted SearXNG instance, prefer HTTPS for non-local endpoints, and avoid submitting secrets or sensitive personal data in queries.

## Reference(s):

- [SearXNG Documentation](https://docs.searxng.org)
- [ClawHub Skill Release](https://clawhub.ai/stperic/skills/local-websearch)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object containing the query, result count, and search result entries with titles, URLs, descriptions, source engines, and relevance scores.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and SEARXNG_URL; result count is clamped from 1 to 20.]

## Skill Version(s):

1.0.0 (source: server release metadata and script __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
