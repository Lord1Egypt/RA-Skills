## Description:

Google Search API returning the full SERP as structured JSON: organic results, ads, knowledge graph, AI Overview, People Also Ask, related searches, top stories and videos. Localize with gl/hl/location, filter by time period, page with start. Also a drop-in Google Custom Search JSON API replacement: same cse.list parameters and items[] response at /customsearch/v1. 1 credit per request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current Google search results and related SERP data as structured JSON, then summarize results with citations. It also supports migration from Google Custom Search JSON API-compatible clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are submitted to Scavio and may contain confidential information.

Mitigation: Remove secrets and unnecessary confidential details from queries; review provider data retention terms before sending sensitive information.

Risk: An exposed API key could be misused.

Mitigation: Store SCAVIO_API_KEY securely and use the Authorization header rather than placing the key in a URL when possible.

Risk: Search requests consume API credits.

Mitigation: Track request volume and remaining credits when using the service.

## Reference(s):

- [Scavio Search API documentation](https://scavio.dev/docs/search-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-search-api)
- [Custom Search compatible endpoint documentation](https://scavio.dev/docs/google-custom-search-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-search-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-search-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis, Guidance]

**Output Format:** [Structured JSON search results and cited Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result sections vary by query; requests consume API credits.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
