## Description: <br>
Pure Python memory management for AI agents with layered memory decay, context compression, memory extraction, vector retrieval, and self-improvement utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[relunctance](https://clawhub.ai/user/relunctance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add persistent task, preference, decision, and document memory to Python-based AI agent workflows. It supports local JSON memory, optional LanceDB retrieval, context compression, and recall workflows across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can store confidential work, credentials, personal data, or agent history. <br>
Mitigation: Review stored memory paths before deployment, restrict filesystem access, and avoid using the skill on shared or sensitive machines unless retention and deletion practices are approved. <br>
Risk: The installer can auto-import existing ~/.openclaw/memory content into the Hawk memory store. <br>
Mitigation: Run installation only after reviewing the import path, or remove or isolate existing memory files before installation if migration is not intended. <br>
Risk: Optional external providers and custom base URLs may receive extracted conversation or memory content. <br>
Mitigation: Use the offline keyword mode or only configure API keys and endpoints that are approved for the data being processed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/relunctance/hawk-memory-v2) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Alert System](references/alerting.md) <br>
- [CLI Reference](references/cli.md) <br>
- [Compression Strategies](references/compression-strategies.md) <br>
- [Context Injection Strategies](references/injection-strategies.md) <br>
- [LanceDB Integration](references/lancedb-integration.md) <br>
- [Four-Tier Memory Architecture](references/memory-system.md) <br>
- [Self-Introspection](references/self-introspection.md) <br>
- [Memory Split Patterns](references/split-patterns.md) <br>
- [Structured Memory Format](references/structured-memory.md) <br>
- [Task State Memory](references/task-state.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update persistent local memory, task state, LanceDB, and governance files under user memory directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
