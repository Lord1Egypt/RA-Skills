## Description:

Search Google Hotels for a destination and dates, then fetch per-property vendor pricing and full details as structured JSON, with price, rating, class, and amenity filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search hotel and vacation-rental options for specific destinations and dates, compare results by price, rating, class, and amenities, and retrieve detailed vendor pricing for selected properties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel searches may send travel dates, destinations, and the Scavio API key to a third-party service.

Mitigation: Confirm the user is comfortable sharing those details with Scavio and keep the API key in an environment variable or secret store.

Risk: Each documented endpoint consumes API credits and repeated searches can create unexpected usage.

Mitigation: Limit calls to needed searches and details, monitor remaining credits, and reuse returned detail tokens when appropriate.

Risk: Hotel names, ratings, prices, vendors, and availability can be misleading if invented or detached from returned API data.

Mitigation: Return only values from API responses, and state the requested stay dates and currency when quoting prices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/google-hotels-api)
- [Scavio Google Hotels API documentation](https://scavio.dev/docs/google-hotels?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-hotels-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=google-hotels-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls, JSON]

**Output Format:** [Markdown guidance with shell commands, Python examples, and structured JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; documented API calls consume 1 credit per request.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
