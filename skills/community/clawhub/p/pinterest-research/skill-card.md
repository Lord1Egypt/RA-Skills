## Description:

Researches Pinterest profiles, boards, pins, ideas categories, and search results via the Crawlora API, returning clean JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, marketers, and content teams use this skill to retrieve public Pinterest profile, board, pin, category, and keyword-search data through Crawlora instead of scraping Pinterest directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pinterest search terms, usernames, board slugs, pin IDs, and the Crawlora API key are sent to Crawlora.

Mitigation: Use the skill only when sharing those inputs with Crawlora is acceptable, keep the key in CRAWLORA_API_KEY, and avoid sensitive or private research terms.

Risk: The skill retrieves public Pinterest data through a third-party service and may reflect that service's availability, limits, and returned data quality.

Mitigation: Review returned JSON before relying on it for decisions, and account for Crawlora API errors, pagination, and credit limits in workflows.

Risk: The helper executes outbound GET requests with credentials.

Mitigation: Use the documented route-limited helper, avoid hardcoding or committing the API key, and review commands before execution.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [Crawlora website](https://crawlora.net)
- [Crawlora API base](https://api.crawlora.net/api/v1)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands that return JSON from the Crawlora API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CRAWLORA_API_KEY and supports documented GET-only Pinterest routes.]

## Skill Version(s):

1.0.17 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
