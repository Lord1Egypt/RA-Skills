## Description: <br>
Free web search and semantic reranking API for AGI applications that need current web information, improved search accuracy, RAG context, or LLM application search integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vaibhav1805](https://clawhub.ai/user/vaibhav1805) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call LangSearch for web search, semantic reranking, and retrieval-augmented generation workflows that need current external context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and reranking documents are sent to the LangSearch API. <br>
Mitigation: Use the skill only for data that may be shared with LangSearch, and avoid submitting sensitive or confidential content unless approved for that service. <br>
Risk: The skill requires a LangSearch API key. <br>
Mitigation: Store LANGSEARCH_API_KEY in environment configuration, keep it out of source control, and monitor account usage. <br>
Risk: Returned web content can contain inaccurate information or instruction-like text. <br>
Mitigation: Treat search results as untrusted context, verify important claims, and do not let returned content override system, developer, or user instructions. <br>


## Reference(s): <br>
- [LangSearch homepage](https://langsearch.com) <br>
- [LangSearch API keys](https://langsearch.com/api-keys) <br>
- [LangSearch API endpoint](https://api.langsearch.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with Python and cURL examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LANGSEARCH_API_KEY and sends search queries or reranking documents to the LangSearch API.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact metadata reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
