## Description:

Real-time web search for AI agents powered by Octen, with result count controls and optional publish-date filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[octenai](https://clawhub.ai/user/octenai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve current web search results for research, news monitoring, and information retrieval workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Octen API key could be forwarded on an HTTP redirect even though the skill intends to use a fixed API endpoint.

Mitigation: Review before installing, use a scoped Octen API key that can be revoked or rotated, and prefer a version that disables redirects or revalidates redirect targets before forwarding authentication headers.

## Reference(s):

- [Octen homepage](https://octen.ai)
- [ClawHub skill page](https://clawhub.ai/octenai/skills/octen-search-skill)
- [Octen publisher profile](https://clawhub.ai/user/octenai)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown text printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OCTEN_API_KEY; supports result count from 1 to 20 and optional ISO 8601 publish-date filters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
