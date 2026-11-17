## Description:

Search the web using Perplexity's Search API for ranked, real-time results with recency filtering, result-count control, and formatted text or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m4vf14](https://clawhub.ai/user/m4vf14)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and external users use this skill to give an OpenClaw agent current web search results for market research, recent news, competitive analysis, and fallback search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Perplexity and may contain sensitive or regulated information.

Mitigation: Use the skill only for queries permitted by your data-handling policy, and avoid confidential or regulated search terms unless approved.

Risk: Use of the skill can incur Perplexity API usage costs.

Mitigation: Monitor Perplexity API usage and configure access only for users or agents authorized to spend against the API key.

Risk: The skill requires PERPLEXITY_API_KEY to be available to the runtime.

Mitigation: Store PERPLEXITY_API_KEY as a secret in the agent environment or OpenClaw configuration, and do not hardcode or log it.

Risk: Formatted output may print remote URLs directly to a terminal or agent transcript.

Mitigation: Review links before opening them and apply normal remote-content handling policies.

## Reference(s):

- [Perplexity API account and usage](https://perplexity.ai/account/api)
- [Perplexity API documentation](https://docs.perplexity.ai)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/m4vf14/skills/perplexity-search-skill)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Formatted terminal text or raw JSON search results containing titles, URLs, snippets, dates, and request metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PERPLEXITY_API_KEY; supports query, result count from 1 to 10, optional recency filter, and a raw JSON mode.]

## Skill Version(s):

1.0.0 (source: skill.json, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
