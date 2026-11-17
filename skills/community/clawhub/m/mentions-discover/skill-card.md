## Description:

Discover the queries worth tracking for a brand's AI visibility, including informational, commercial, and comparison-intent prompts, via MentionsAPI.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and brand-monitoring teams use this skill when they explicitly need candidate prompts or questions to track for a brand's AI visibility program. It returns query suggestions that can be checked or monitored with related MentionsAPI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate paid MentionsAPI query-discovery calls using MENTIONSAPI_KEY.

Mitigation: Confirm the brand and, when available, the industry before each call and use the skill only when the user explicitly asks for query suggestions.

Risk: The API key and brand query are sent to the disclosed MentionsAPI endpoint.

Mitigation: Install only when you intend to use MentionsAPI and are comfortable providing MENTIONSAPI_KEY for this purpose.

Risk: The documentation mentions an optional unpinned npx MCP alternative.

Mitigation: Avoid that alternative unless the package is separately trusted and pinned.

## Reference(s):

- [MentionsAPI homepage](https://mentionsapi.com)
- [MentionsAPI endpoint reference](https://mentionsapi.com/docs/api/check)
- [MentionsAPI OpenAPI spec](https://mentionsapi.com/openapi.json)
- [ClawHub skill page](https://clawhub.ai/nikhonit/skills/mentions-discover)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Guidance]

**Output Format:** [Python dict / JSON-compatible response containing candidate queries, intents, cost information, or structured error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MENTIONSAPI_KEY and sends the confirmed brand query to MentionsAPI. The count parameter supports 1-100 results and defaults to 50.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
