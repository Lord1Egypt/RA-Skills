## Description: <br>
Set up local semantic memory search in OpenClaw using Ollama and nomic-embed-text so embeddings can run privately without a cloud API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spmzt](https://clawhub.ai/user/spmzt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure local semantic memory search with Ollama, including setup commands, provider settings, and troubleshooting guidance for offline-capable embeddings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Additional Markdown directories configured through extraPaths may make private or shared notes searchable. <br>
Mitigation: Include only directories that are intended for memory search, and review extraPaths before enabling recursive indexing. <br>
Risk: Incorrect provider or baseUrl settings can prevent local Ollama search from working as intended. <br>
Mitigation: Use provider "ollama" and baseUrl "http://127.0.0.1:11434", then restart the OpenClaw gateway after changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/spmzt/ollama-memory-with-freebsd) <br>
- [Ollama](https://ollama.ai/) <br>
- [Configuration Reference](references/config-reference.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Ollama and curl; metadata lists linux, darwin, win32, and freebsd support.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
