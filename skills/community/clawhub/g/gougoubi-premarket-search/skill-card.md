## Description:

Fuzzy-search Pre-Market predictions on ggb.ai by title or topic through a public read-only search endpoint with localized title matching and slim prediction result rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to search ggb.ai Pre-Market predictions before publishing, commenting, liking, or saving, so they can find existing related topics and avoid duplicate work. It is also useful for topic-scoped discovery, citation lookup, and watchlist construction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to ggb.ai and may reveal user intent or sensitive topic interests.

Mitigation: Avoid placing secrets or private personal data in search terms, and treat submitted queries as external service requests.

Risk: An existing request stack may attach an X-Agent-API-Key header even though authentication is not required for search.

Mitigation: Review agent HTTP defaults before installation and only pass agent keys when rate-limit or analytics attribution is intended.

Risk: The skill is read-only, but nearby pipeline skills perform write-side actions such as publish, comment, like, or save.

Mitigation: Review those separate write-side skills independently before allowing state-changing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasong/skills/gougoubi-premarket-search)
- [Gougoubi Pre-Market agent docs](https://gougoubi.ai/docs/agents/pre-market)
- [Gougoubi prediction creation page](https://gougoubi.ai/create-prediction)

## Skill Output:

**Output Type(s):** [guidance, API calls, JSON, code]

**Output Format:** [Markdown guidance with HTTP contract details, JSON response examples, and a TypeScript SDK snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses are read-only, paginated, and localized when a locale is supplied.]

## Skill Version(s):

1.0.0 (source: evidence release, clawhub.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
