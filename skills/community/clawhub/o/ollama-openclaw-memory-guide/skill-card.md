## Description: <br>
Guides Windows users through installing portable Ollama and configuring OpenClaw local memory search with vector indexing and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators in managed Windows environments use this skill to set up local Ollama embeddings for OpenClaw memory search, rebuild vector indexes, configure startup behavior, and troubleshoot common failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local vector indexing may process confidential OpenClaw memory files. <br>
Mitigation: Review memory contents before rebuilding the index and protect or delete generated backups and SQLite stores according to local data-handling requirements. <br>
Risk: The optional Startup VBS runs Ollama silently at each Windows sign-in. <br>
Mitigation: Enable the startup script only when persistent local Ollama service is desired, and remove the Startup entry when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/ollama-openclaw-memory-guide) <br>
- [Ollama documentation](https://ollama.com/docs) <br>
- [OpenClaw memory documentation](https://docs.openclaw.ai/memory) <br>
- [TDaí Memory Suite](https://clawhub.ai/skills/tdai-memory-suite) <br>
- [nomic-embed-text model](https://ollama.com/library/nomic-embed-text) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guide with PowerShell, bash, JSON, Python, SQL, and VBS snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Windows setup steps, OpenClaw configuration examples, vector index rebuild guidance, startup script examples, troubleshooting checks, and backup and restore procedures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, SKILL.md version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
