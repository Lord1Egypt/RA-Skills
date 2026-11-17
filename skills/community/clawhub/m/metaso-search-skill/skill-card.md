## Description:

Search the web using Metaso AI Search API for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[square123](https://clawhub.ai/user/square123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Metaso AI Search for current web, news, paper, documentation, and research results through a Python command backed by a Metaso API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, selected request options, and the Metaso API bearer token are sent to Metaso's API.

Mitigation: Avoid submitting private secrets or sensitive personal data in queries, and use a tighter runtime permission policy when the agent environment supports one.

## Reference(s):

- [Metaso Search API Playground](https://metaso.cn/search-api/playground)
- [Metaso Search API Endpoint](https://metaso.cn/api/v1/search)
- [ClawHub Skill Page](https://clawhub.ai/square123/skills/metaso-search-skill)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON response from the Metaso API, or plain-text error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires METASO_API_KEY; request options include q, scope, size, page, conciseSnippet, includeSummary, and includeRawContent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
