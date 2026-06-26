## Description: <br>
Web search via Ollama API. Returns relevant results from Ollama web search for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cndaqiang](https://clawhub.ai/user/cndaqiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to send search queries to Ollama Web Search and receive JSON results for grounding, discovery, and research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Ollama using the configured OLLAMA_API_KEY. <br>
Mitigation: Use only with queries approved for Ollama, and keep OLLAMA_API_KEY managed as a secret. <br>
Risk: The packaged _meta.json version differs from the server release version. <br>
Mitigation: Verify the ClawHub release page or registry entry when exact version provenance matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cndaqiang/ollama-web-search) <br>
- [Ollama Web Search API](https://ollama.com/api/web_search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and OLLAMA_API_KEY; max_results is clamped from 1 to 10.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
