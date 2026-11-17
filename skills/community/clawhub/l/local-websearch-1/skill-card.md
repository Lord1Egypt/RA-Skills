## Description:

Search the web using a self-hosted SearXNG metasearch engine that aggregates multiple sources without API keys and returns structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eg-yks](https://clawhub.ai/user/eg-yks)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to route current-information web searches through a self-hosted SearXNG endpoint and receive structured search results. It is useful when API keys are unavailable or when search traffic should be directed to an operator-controlled metasearch service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the SearXNG service configured in SEARXNG_URL and may be visible to that server and its logs.

Mitigation: Use only a trusted SearXNG endpoint and avoid sending sensitive queries unless that endpoint's logging and retention practices are acceptable.

Risk: The setup example allows a plaintext HTTP SearXNG endpoint.

Mitigation: Prefer an HTTPS SearXNG URL before enabling the skill for routine use.

Risk: Credentials or tokens embedded in SEARXNG_URL could be exposed through configuration or logs.

Mitigation: Do not put credentials in the URL; use endpoint-level access controls that do not require secrets in environment variable values.

Risk: Operational reliability depends on the local package layout and command path matching the skill metadata.

Mitigation: Verify the installed package layout and command path before relying on the skill operationally.

## Reference(s):

- [SearXNG documentation](https://docs.searxng.org)
- [ClawHub skill page](https://clawhub.ai/eg-yks/skills/local-websearch-1)
- [Publisher profile](https://clawhub.ai/user/eg-yks)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON search results with query, count, result titles, URLs, descriptions, source engines, and relevance scores.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the SEARXNG_URL environment variable; result count is constrained to 1-20.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
