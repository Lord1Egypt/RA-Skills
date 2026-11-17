## Description:

Free web search and semantic reranking API for AGI applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vaibhav1805](https://clawhub.ai/user/vaibhav1805)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add current web search, semantic reranking, and RAG context-gathering examples to LLM applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, reranking documents, and the LangSearch API key are sent to LangSearch over HTTPS.

Mitigation: Keep the API key in an environment variable and avoid confidential queries unless LangSearch's data handling terms meet the deployment's needs.

Risk: The skill depends on a valid LangSearch API key and external API availability.

Mitigation: Configure LANGSEARCH_API_KEY before use and handle authorization, rate-limit, timeout, and server-error responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vaibhav1805/skills/langsearch)
- [LangSearch homepage](https://langsearch.com)
- [LangSearch API keys](https://langsearch.com/api-keys)
- [LangSearch API base endpoint](https://api.langsearch.com/v1)
- [LangSearch web search endpoint](https://api.langsearch.com/v1/web-search)
- [LangSearch rerank endpoint](https://api.langsearch.com/v1/rerank)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LANGSEARCH_API_KEY and sends requests to the LangSearch API over HTTPS.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
