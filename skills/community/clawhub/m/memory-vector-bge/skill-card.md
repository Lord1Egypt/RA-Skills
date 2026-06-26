## Description: <br>
Provides BGE-M3-based automatic log distillation into vector memory with semantic similarity search and automatic core-memory updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duzhilei951](https://clawhub.ai/user/duzhilei951) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to maintain a local multi-layer memory system that distills recent conversation logs into vector-searchable memories and updates core memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory logs, search queries, and embeddings may be sent to configured embedding or LLM services. <br>
Mitigation: Use local-only endpoints when possible, review endpoint configuration before running, and do not use the skill with secrets or sensitive conversations. <br>
Risk: Personal profile details and distilled memories may be stored locally in memory and vector files. <br>
Mitigation: Review generated memory files regularly, remove sensitive entries, and clear API keys from persisted configuration before sharing or archiving the workspace. <br>
Risk: The server security verdict is suspicious because consent safeguards for persisted memory data are not clear. <br>
Mitigation: Run the skill only after explicit user approval for memory capture and storage, and document what data will be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duzhilei951/memory-vector-bge) <br>
- [Configuration defaults](artifact/references/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript command-line scripts and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local memory files, vector JSON data, tags, summaries, importance scores, and search results.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
