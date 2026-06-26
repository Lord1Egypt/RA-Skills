## Description: <br>
Memory Core provides long-term vector memory storage and retrieval for OpenClaw agents with intent and scene isolation to reduce memory contamination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilei0311](https://clawhub.ai/user/lilei0311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw agent builders use this skill to store, retrieve, and forget long-term user facts across sessions while filtering retrieval by agent and scene. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-term memory may contain private user facts that are sent to a remote embedding provider when cloud embeddings are configured. <br>
Mitigation: Use a local embedding backend for sensitive memory and restrict any remote endpoint to a provider you trust. <br>
Risk: Embedding credentials may be read from local configuration or environment variables and could be shared unintentionally. <br>
Mitigation: Avoid shared or global API keys unless intended, and review local OpenClaw and environment configuration before installation. <br>
Risk: Memory database upgrades or schema changes can affect stored long-term memory. <br>
Mitigation: Keep backups of the LanceDB memory database before upgrades or schema changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lilei0311/memory-core) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/lilei0311) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON CLI responses and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Retrieval output can be limited by configured per-memory and total character budgets.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
