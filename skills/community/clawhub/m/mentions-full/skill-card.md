## Description:

Complete AI brand-visibility toolkit via MentionsAPI.com. Four tools \u2014 check mentions/ranks/citations across ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews/AI Mode, and Bing Copilot; discover queries to track; compare two brands or queries; and watch for changes over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to measure a brand's visibility in AI-generated answers, discover tracking queries, compare brand or query performance, and monitor mention, rank, or citation changes over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a MentionsAPI key and paid API calls, so use can expose account credentials and consume wallet balance.

Mitigation: Install only if comfortable providing a MentionsAPI key, confirm user intent before credit-consuming calls, and monitor account balance.

Risk: The persistent watch_brand monitor can send sensitive brand-visibility data to unsafe webhook destinations and may create ongoing charges.

Mitigation: Use only an HTTPS webhook endpoint you control, use a strong secret, verify HMAC signatures, reject replayed deliveries, rotate leaked secrets, and confirm how to disable monitors.

## Reference(s):

- [MentionsAPI Homepage](https://mentionsapi.com)
- [MentionsAPI Endpoint Reference](https://mentionsapi.com/docs/api/check)
- [MentionsAPI OpenAPI Specification](https://mentionsapi.com/openapi.json)
- [MentionsAPI Recipes](https://mentionsapi.com/docs/recipes)
- [ClawHub Skill Page](https://clawhub.ai/nikhonit/skills/mentions-full)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Guidance]

**Output Format:** [JSON-compatible Python dictionaries with API responses and error objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MENTIONSAPI_KEY and consumes MentionsAPI credits for paid calls.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
