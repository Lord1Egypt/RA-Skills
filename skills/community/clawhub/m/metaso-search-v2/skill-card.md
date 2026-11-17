## Description:

Provides direct access to the Metaso Search API for web search, webpage reading, and RAG-style question answering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinmh1338863](https://clawhub.ai/user/xinmh1338863)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to route search, webpage reading, and chat-answering requests through Metaso when an agent needs external web results or URL content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided searches, URLs, and chat messages are sent to Metaso as an external service.

Mitigation: Use the skill only when disclosure to Metaso is acceptable, and avoid sending secrets, private internal URLs, or sensitive personal data.

Risk: The skill requires a Metaso API key for authenticated requests.

Mitigation: Provide METASO_API_KEY through environment configuration and do not hard-code or commit the key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xinmh1338863/skills/metaso-search-v2)
- [Metaso search API endpoint](https://metaso.cn/api/v1/search)
- [Metaso reader API endpoint](https://metaso.cn/api/v1/reader)
- [Metaso chat completions API endpoint](https://metaso.cn/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [JSON, Markdown, or plain text returned from Metaso API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires METASO_API_KEY; responses depend on the selected Metaso operation, scope, model, and requested format.]

## Skill Version(s):

2.1.0 (source: evidence.release.version, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
