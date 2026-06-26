## Description: <br>
Use when user wants to integrate Ollama into coding agents, IDEs, or agent harnesses. Supports local/on-prem/Docker deployment, Ollama Cloud, OpenAI/Anthropic-compatible endpoints, streaming, structured outputs, embeddings, tool calling, and web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waiyannyeinnaing](https://clawhub.ai/user/waiyannyeinnaing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to wire Ollama into coding agents, IDE integrations, and backend agent harnesses across local, on-prem, Docker, and Ollama Cloud deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install metadata declares purchase and crypto capabilities that do not match the Ollama integration guidance. <br>
Mitigation: Before installing, confirm those capabilities are intended or remove them if they affect platform permissions. <br>
Risk: Remote Ollama endpoints and OLLAMA_API_KEY can send prompts or code to a cloud provider. <br>
Mitigation: Use localhost or trusted hosts for sensitive work, reserve OLLAMA_API_KEY for intended cloud calls, and handle it as a secret. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/waiyannyeinnaing/ollama-skill) <br>
- [Ollama API](https://ollama.com/api) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with code snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include runnable examples, environment variable guidance, adapter code, and local/cloud switching notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, _meta.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
