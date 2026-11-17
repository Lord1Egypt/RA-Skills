## Description:

AI-optimized web search via AIsa's Tavily API proxy, returning concise and relevant results for AI agents through AIsa's unified API gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to run web searches, news searches, deeper research queries, and URL content extraction through AIsa's Tavily API proxy. It is intended for concise source discovery and page-content retrieval inside an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, extraction URLs, and AISA_API_KEY-authenticated requests are sent to AIsa.

Mitigation: Use the skill only when that data sharing is acceptable; avoid private/internal URLs, signed links, URLs containing credentials, and sensitive queries.

Risk: URL extraction can be misused against paywalled or subscription-gated content.

Mitigation: Do not extract from paywalled or access-controlled sites; use proper subscriptions, institutional access, or publisher-approved licensing instead.

Risk: Redundant query variations can waste API quota and increase unnecessary data transmission.

Mitigation: Consolidate overlapping searches into two or three focused queries before running the tool.

Risk: Search results or extracted content may be inappropriately transmitted to external endpoints.

Mitigation: Keep retrieved content in the agent conversation and let the user decide how to share it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/openclaw-aisa-web-search-tavily-hardened)
- [AIsa](https://aisa.one)
- [AIsa marketplace](https://marketplace.aisa.one)
- [Faberlens safety evaluation](https://faberlens.ai/explore/openclaw-aisa-web-search-tavily)
- [SAFETY.md](SAFETY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with search answers, source lists, extracted page content, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and AISA_API_KEY; search result count is capped at 20 by the script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
