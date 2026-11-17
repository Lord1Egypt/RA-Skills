## Description:

Memory Plus helps agents save, search, deduplicate, prune, consolidate, and list persistent memories with local file and FTS5 storage plus optional knowledge graph, embedding, and Milvus backends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liushuangfa666](https://clawhub.ai/user/liushuangfa666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an agent persistent memory across sessions, including command-driven storage, retrieval, cleanup, consolidation, and optional full-session saving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent always-on memory can search or save prior user content without enough scoping.

Mitigation: Review the installation rules before enabling the skill, prefer explicit memory commands, and scope where the skill is installed.

Risk: Complete conversations and sensitive text can be stored in local memory files and indexes.

Mitigation: Avoid saving secrets or sensitive conversations, periodically prune stored memories, and review saved memory files before sharing an environment.

Risk: Stored text can be sent to configured Ollama, embedding, or Milvus services.

Mitigation: Disable or firewall remote backends unless needed, and use only trusted local or approved service endpoints.

## Reference(s):

- [ClawHub memory-plus release page](https://clawhub.ai/liushuangfa666/skills/memory-plus)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions, shell commands, and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown memory files, SQLite indexes, and optional records in configured knowledge graph or Milvus stores.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
