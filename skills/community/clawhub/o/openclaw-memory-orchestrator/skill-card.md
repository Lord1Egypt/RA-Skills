## Description: <br>
OpenClaw Memory Orchestrator provides memory optimization, compression, deduplication, layered indexing, and adaptive retrieval routing for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[che52078](https://clawhub.ai/user/che52078) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to maintain cleaner OpenClaw long-term memory through compression, deduplication, canonicalization, layered retrieval views, and adaptive retrieval routing. It supports local-only operation by default, with optional Ollama and remote vector database modes when explicitly configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional remote and mem0 sync can export internal memory summaries and metadata to remote backends, including plain HTTP endpoints. <br>
Mitigation: Use local-only mode unless remote sync is required; when remote sync is enabled, use HTTPS-only trusted endpoints and review records marked internal before syncing. <br>
Risk: Persistent local memory indexes under the OpenClaw workspace may retain sensitive project or conversation context. <br>
Mitigation: Limit workspace scope, review generated memory records and reports, and apply retention or cleanup practices before sharing a workspace or machine. <br>
Risk: The skill depends on chromadb for local vector storage. <br>
Mitigation: Pin and review the chromadb dependency before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/che52078/openclaw-memory-orchestrator) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, and generated JSON or Markdown memory reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local OpenClaw workspace memory indexes, retrieval views, reports, and sync state when scripts are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
