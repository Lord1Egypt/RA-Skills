## Description: <br>
MindGardener provides local-first long-term memory for autonomous agents by creating wiki knowledge graphs from conversations, scoring events by surprise, detecting conflicts, and assembling token-budget context for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[widingmarcus-cyber](https://clawhub.ai/user/widingmarcus-cyber) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use MindGardener to give autonomous agents persistent file-based memory, turning conversation logs into entity pages, graph triplets, conflict and surprise signals, and recall context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive memory logs may be sent to external LLM providers during extraction, surprise scoring, consolidation, beliefs, or nightly jobs. <br>
Mitigation: Use a local provider such as Ollama for private data, and review provider configuration before running commands that perform model-assisted processing. <br>
Risk: The tool can read, rewrite, sync, and persist model-derived workspace memory files. <br>
Mitigation: Review generated MEMORY.md, entity pages, and context outputs before relying on them, and use caution with sync, write-back, and automated --apply workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/widingmarcus-cyber/mindgardener) <br>
- [MindGardener GitHub Repository](https://github.com/widingmarcus-cyber/mindgardener) <br>
- [MindGardener PyPI Project](https://pypi.org/project/mindgardener/) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>
- [Research Background](docs/RESEARCH.md) <br>
- [State Tracker Integration](docs/state-tracker-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets, YAML configuration, and generated Markdown and JSONL memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates file-based memory artifacts such as MEMORY.md, memory/entities/*.md, graph.jsonl, RECALL-CONTEXT.md, and garden.yaml; some commands can call configured LLM providers.] <br>

## Skill Version(s): <br>
1.1.0 (source: release metadata, pyproject.toml, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
