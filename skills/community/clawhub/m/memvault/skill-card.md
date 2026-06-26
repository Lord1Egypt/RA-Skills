## Description: <br>
MemVault provides a Docker-based long-term memory server for AI agents with Ebbinghaus decay, strength-weighted retrieval, memory statistics, and multi-agent tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjy9902](https://clawhub.ai/user/wjy9902) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent operators use MemVault to add persistent, searchable memory to AI agents across sessions, including local storage, retrieval, decay, and statistics workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent storage of conversation-derived memory can retain sensitive or private information. <br>
Mitigation: Avoid storing secrets, regulated data, or private conversations until retention and deletion controls are in place. <br>
Risk: The service exposes unauthenticated local endpoints and default database credentials. <br>
Mitigation: Bind services to localhost only, change default database credentials, and add authentication or firewall controls before broader use. <br>
Risk: The installer can run setup steps that affect the local environment. <br>
Mitigation: Review the installer before execution and consider installing dependencies such as Ollama manually. <br>


## Reference(s): <br>
- [ClawHub MemVault release](https://clawhub.ai/wjy9902/memvault) <br>
- [Docker installation documentation](https://docs.docker.com/get-docker/) <br>
- [Ollama download](https://ollama.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API payload examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Docker Compose, CLI, HTTP API, and environment variable guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
