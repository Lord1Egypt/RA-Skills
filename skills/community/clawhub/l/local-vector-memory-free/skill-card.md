## Description: <br>
Local Vector Memory Free helps agents set up and operate a local vector-memory workflow using Ollama and LanceDB for offline embedding, local storage, and basic semantic retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure and operate a local long-term memory layer for preferences, notes, and project context while keeping embeddings and vector data on the local machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can capture sensitive personal, medical, regulated, or secret information. <br>
Mitigation: Store only consented, non-secret information; avoid credentials and regulated records unless there is an explicit retention and deletion plan. <br>
Risk: Memory files, vector data, exports, and backups can retain stale or unintended records after the original session ends. <br>
Mitigation: Review SESSION-STATE.md, MEMORY.md, memory logs, vector data, exports, and backups regularly, and require confirmation before cleanup or forget operations. <br>
Risk: Configuring a remote Ollama endpoint can move embedding inputs outside the local machine. <br>
Mitigation: Use a local Ollama endpoint for privacy-sensitive data, and document remote endpoint controls before enabling OLLAMA_HOST. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/local-vector-memory-free) <br>
- [Ollama download](https://ollama.com/download) <br>
- [Node.js](https://nodejs.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command results may include text, JSON, or CSV depending on the requested memory operation and output_format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
