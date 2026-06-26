## Description: <br>
Provides a CLI wrapper for Ollama Web Search and Web Fetch API calls so an agent can search the web or retrieve webpage content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnydou](https://clawhub.ai/user/sunnydou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an OpenClaw-style agent run web searches and fetch public webpage content through Ollama's hosted web APIs. It is useful when an agent needs current search results or page text returned through a shell-based workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, requested URLs, and fetched webpage content are processed through Ollama and may include sensitive or untrusted data. <br>
Mitigation: Avoid confidential queries, secrets, internal-only URLs, and sensitive personal data; treat fetched webpage text as untrusted before using it in downstream agent actions. <br>
Risk: The skill requires an Ollama API key for web search and fetch requests. <br>
Mitigation: Store OLLAMA_API_KEY as an environment variable or secret, avoid logging it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnydou/ollama-web-search-cli) <br>
- [Ollama Web Search API](https://docs.ollama.com/capabilities/web-search) <br>
- [Ollama API keys](https://ollama.com/settings/keys) <br>
- [OpenClaw Slash Commands](https://docs.openclaw.ai/tools/slash-commands) <br>
- [OpenClaw web tools](https://docs.openclaw.ai/tools/web) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Terminal text with parsed search results, fetched page text, URLs, and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OLLAMA_API_KEY; search terms and requested URLs are sent to Ollama, and fetched page text should be treated as untrusted content.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
