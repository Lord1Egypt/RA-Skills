## Description: <br>
Graph-RAG Memory provides persistent, queryable long-term memory for OpenClaw agents using Graphiti, FalkorDB, local Ollama embeddings, and a MoE-style multi-embedding router. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jebadiahgreenwood](https://clawhub.ai/user/jebadiahgreenwood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, configure, query, and maintain a persistent graph-RAG memory system for agent conversations, documents, and project facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent ingestion can add workspace files, notes, or personal data to the memory graph. <br>
Mitigation: Run the installer with --dry-run first, review and minimize the seed set, and exclude secrets or personal data before enabling broad workspace ingestion. <br>
Risk: Installation can modify OpenClaw configuration. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before installation and review the configuration changes before restarting OpenClaw. <br>
Risk: Background refresh behavior can run through a daemon or silent scheduled job. <br>
Mitigation: Do not start memwatchd or configure a silent cron job until the referenced runtime files are present and reviewed; monitor the PID and logs if enabled. <br>
Risk: The skill depends on local services and models whose endpoints may expose or process sensitive workspace content. <br>
Mitigation: Confirm FalkorDB and Ollama endpoints are local and intended, and use the status script to verify models and graph state before use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jebadiahgreenwood/graph-rag-memory) <br>
- [Setup & Environment Reference](references/setup.md) <br>
- [Research Foundations & Citations](references/research.md) <br>
- [Publishing to ClawHub](references/clawhub.md) <br>
- [RouterRetriever](https://arxiv.org/abs/2409.02685) <br>
- [Graphiti](https://www.getzep.com/graphiti) <br>
- [FalkorDB](https://github.com/FalkorDB/FalkorDB) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, plus optional JSON status and query output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on local OpenClaw, FalkorDB, Ollama, and workspace memory state.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
