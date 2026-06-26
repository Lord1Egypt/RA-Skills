## Description: <br>
An agent memory workflow for storing, searching, deduplicating, pruning, and consolidating cross-chat memories with local files, SQLite FTS5, a knowledge graph, and optional vector storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liushuangfa666](https://clawhub.ai/user/liushuangfa666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to give an agent persistent memory across conversations, retrieve relevant prior notes, and maintain the memory store through deduplication, pruning, consolidation, and listing tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on cross-chat memory retrieval can surface saved personal, sensitive, or stale conversation content in later sessions. <br>
Mitigation: Review and edit the AGENTS.md rule before installation, save only intended information, and avoid storing secrets or sensitive conversations. <br>
Risk: Persistence and maintenance tools can modify or delete memory files, including prune and cleanup behavior. <br>
Mitigation: Back up the memory directory before using prune, deduplication, consolidation, or cleanup workflows. <br>
Risk: Optional Ollama, embedding, rerank, and Milvus integrations send memory content to configured local or network endpoints. <br>
Mitigation: Use only trusted endpoints and confirm host, port, and model configuration before enabling optional services. <br>
Risk: An incorrect install path or copied rule can cause memory search or save commands to run against the wrong workspace. <br>
Mitigation: Confirm the installed path and command snippets before applying the AGENTS.md configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liushuangfa666/memory-plus) <br>
- [Publisher profile](https://clawhub.ai/user/liushuangfa666) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell command snippets, and JSON or plain-text CLI/tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists memory entries under the user's OpenClaw workspace and can use optional local Ollama, embedding, rerank, or Milvus endpoints when configured.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
