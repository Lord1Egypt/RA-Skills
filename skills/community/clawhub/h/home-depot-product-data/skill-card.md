## Description:

Search Home Depot, pull full item detail and page through review bodies as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to search Home Depot products, retrieve item details, and collect paginated reviews for price monitoring, catalog enrichment, and review analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests share Home Depot search terms, item IDs, and the API key with Scavio.

Mitigation: Install only if this data sharing is acceptable, keep SCAVIO_API_KEY scoped and revocable, and use an isolated environment for optional SDK usage.

Risk: Repeated or paginated calls can consume Scavio credits unexpectedly.

Mitigation: Set page limits before loops, monitor credit usage, and avoid retrying invalid item IDs or review pages past total_pages.

## Reference(s):

- [Scavio Home Depot Search Documentation](https://scavio.dev/docs/home-depot-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=home-depot-product-data)
- [Scavio Rate Limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=home-depot-product-data)
- [ClawHub Skill Page](https://clawhub.ai/scavio-ai/skills/home-depot-product-data)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON API responses and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; Home Depot endpoints return structured JSON.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
