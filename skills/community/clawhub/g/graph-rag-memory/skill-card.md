## Description:

Graph-RAG Memory provides persistent, queryable long-term memory for OpenClaw agents using a Graphiti temporal knowledge graph, FalkorDB, local Ollama embeddings, and MoE-style multi-embedding routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jebadiahgreenwood](https://clawhub.ai/user/jebadiahgreenwood)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent operators use this skill to install and operate persistent agent memory, ingest workspace content or text into a graph, query remembered facts, and check memory system status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist and index workspace data in FalkorDB.

Mitigation: Inspect what will be ingested, scope the workspace deliberately, and run installation with --dry-run and --skip-seed before enabling ingestion.

Risk: The installer can patch OpenClaw configuration and run mutable workspace scripts.

Mitigation: Review install.sh and the memory-upgrade implementation files first, back up configuration, and add dependency pinning before production use.

Risk: The background watcher and recurring refresh can ingest changed Markdown files automatically.

Mitigation: Do not enable the daemon or recurring refresh until workspace scoping, stop/uninstall controls, and operational monitoring are in place.

## Reference(s):

- [Setup & Environment Reference](references/setup.md)
- [Research Foundations & Citations](references/research.md)
- [RouterRetriever](https://arxiv.org/abs/2409.02685)
- [Graphiti](https://github.com/getzep/graphiti)
- [Graphiti Blog](https://www.getzep.com/graphiti)
- [FalkorDB](https://github.com/FalkorDB/FalkorDB)
- [ClawHub Skill Page](https://clawhub.ai/jebadiahgreenwood/skills/graph-rag-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may install dependencies, update local configuration, ingest workspace memory files, query FalkorDB, and start a background file watcher.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
