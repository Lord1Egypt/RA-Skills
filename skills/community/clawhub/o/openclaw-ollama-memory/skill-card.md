## Description: <br>
Set up local semantic memory search in OpenClaw using Ollama and nomic-embed-text, replacing cloud embedding APIs with a locally running model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure local, offline-capable semantic memory search with Ollama embeddings and no external API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexing additional paths may include private directories in local memory search. <br>
Mitigation: Review every extraPaths entry before enabling it and limit indexing to intended markdown directories. <br>
Risk: The OpenClaw configuration change and downloaded Ollama model persist after setup. <br>
Mitigation: Remove the memorySearch configuration and downloaded model when local embedding search is no longer wanted. <br>
Risk: Pointing the base URL away from localhost can route embedding requests outside the intended local Ollama service. <br>
Mitigation: Keep remote.baseUrl set to http://127.0.0.1:11434 unless an explicitly trusted local service is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/djc00p/openclaw-ollama-memory) <br>
- [Ollama](https://ollama.ai) <br>
- [Configuration Reference](references/config-reference.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces configuration steps for OpenClaw memorySearch, Ollama model setup commands, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
