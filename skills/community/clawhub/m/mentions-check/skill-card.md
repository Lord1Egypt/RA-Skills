## Description:

Check whether a brand is mentioned, ranked, and cited across AI search surfaces including ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews/AI Mode, and Bing Copilot via MentionsAPI.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to measure whether a specific brand appears, how it ranks, and what citations are returned for a chosen AI-search query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand visibility checks send the tested query, brand name, selected mode, and API key to MentionsAPI.

Mitigation: Use the skill only for explicit visibility checks, avoid sensitive query text, and configure MENTIONSAPI_KEY only in trusted agent environments.

Risk: Each check can consume MentionsAPI credits, and live modes or repeated runs increase cost.

Mitigation: Confirm ambiguous requests before calling the tool, start with the quick mode when appropriate, and choose runs and live modes deliberately.

Risk: The separately mentioned hosted MCP alternative introduces package supply-chain risk if used.

Mitigation: Use a pinned and reviewed MCP package version when choosing that alternative instead of this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nikhonit/skills/mentions-check)
- [MentionsAPI homepage](https://mentionsapi.com)
- [MentionsAPI check endpoint reference](https://mentionsapi.com/docs/api/check)
- [MentionsAPI OpenAPI specification](https://mentionsapi.com/openapi.json)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Python dict or JSON-like response containing per-surface mention, rank, citation, cost, balance, cache, or error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MENTIONSAPI_KEY and sends user-requested brand visibility checks to MentionsAPI; calls may consume credits.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
