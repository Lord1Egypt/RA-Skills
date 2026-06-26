## Description: <br>
Web reading and searching via Jina AI APIs, including clean markdown extraction from URLs, web search, and deep multi-step research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adhishthite](https://clawhub.ai/user/adhishthite) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to fetch web pages or PDFs as markdown, run web searches, and perform multi-step research through Jina AI APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided URLs, search terms, research prompts, and JINA_API_KEY-authenticated requests are sent to Jina AI. <br>
Mitigation: Use the skill only with data approved for Jina AI, and avoid secrets, private internal URLs, or confidential research unless Jina is approved for that data. <br>
Risk: The JINA_API_KEY can be exposed if it is committed, shared, or logged. <br>
Mitigation: Store JINA_API_KEY in an environment variable or secret manager, and do not commit or share it. <br>
Risk: Reader, search, and DeepSearch outputs can reflect incomplete, stale, or third-party web content. <br>
Mitigation: Review important results against authoritative sources before relying on them for decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/adhishthite/jina-ai) <br>
- [Publisher Profile](https://clawhub.ai/user/adhishthite) <br>
- [Jina AI](https://jina.ai/) <br>
- [Jina Reader](https://jina.ai/reader) <br>
- [Jina Search Documentation](https://s.jina.ai/docs) <br>
- [Reader OpenAPI Specification](https://r.jina.ai/openapi.json) <br>
- [Search OpenAPI Specification](https://s.jina.ai/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON returned to stdout, with shell command examples and guidance for configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JINA_API_KEY and sends user-provided URLs, search queries, or research prompts to Jina AI endpoints.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
