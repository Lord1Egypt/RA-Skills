## Description:

Real-time web search for AI agents powered by Octen. Fast, fresh, and relevant - search the web, filter by date, and get LLM-ready results in under 80ms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jac9935](https://clawhub.ai/user/jac9935)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to search the live web, retrieve recent results, and filter results by publish-time windows for research, news monitoring, and current-information tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OCTEN_API_KEY may be carried by automatic redirects from the Octen API endpoint.

Mitigation: Use a limited, revocable Octen API key, monitor key usage, and review redirect handling before relying on the endpoint-only credential claim.

Risk: Search queries and result requests are sent to Octen's external service.

Mitigation: Use the skill only when the user trusts Octen with the submitted queries and avoid sending sensitive or confidential search text.

## Reference(s):

- [Octen](https://octen.ai)
- [Octen Search API endpoint](https://api.octen.ai/search)
- [ClawHub skill page](https://clawhub.ai/jac9935/skills/octen-search-skills)
- [Publisher profile](https://clawhub.ai/user/jac9935)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown search results containing result titles, URLs, optional publication times, and highlights.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result count is clamped from 1 to 20; optional start_time and end_time filters are sent to Octen when provided.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
