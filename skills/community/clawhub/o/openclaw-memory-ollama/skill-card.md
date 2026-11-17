## Description:

OpenClaw local memory management guidance for building a long-term AI memory setup with Ollama embeddings, cognitive-brain structured storage, PostgreSQL, Redis, and memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haven-ops](https://clawhub.ai/user/haven-ops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure local OpenClaw memory search and long-term memory storage with Ollama, cognitive-brain, PostgreSQL, Redis, and local files. It also supports troubleshooting memory retrieval and embedding setup issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent AI memory may store sensitive conversation content indefinitely.

Mitigation: Use non-sensitive test data first, define what may be stored, and document deletion and export procedures before production use.

Risk: The configuration guidance can affect global OpenClaw model settings beyond memory search.

Mitigation: Merge only the memorySearch settings unless an intentional global model provider change has been reviewed.

Risk: Local memory retrieval depends on Ollama, PostgreSQL with pgvector, Redis, and cognitive-brain being configured consistently.

Mitigation: Run the documented service checks and embedding warmup before relying on memory recall.

## Reference(s):

- [Openclaw Memory Ollama on ClawHub](https://clawhub.ai/haven-ops/skills/openclaw-memory-ollama)
- [Architecture Reference](references/architecture.md)
- [Deployment Guide](references/deployment.md)
- [Configuration Reference](references/config-reference.md)
- [cognitive-brain](https://clawhub.ai/skills/cognitive-brain)
- [Ollama](https://ollama.ai/)
- [pgvector](https://github.com/pgvector/pgvector)
- [lark-whiteboard](https://clawhub.ai/skills/lark-whiteboard)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline bash, JSON, SQL, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local deployment, configuration, validation, and troubleshooting guidance for OpenClaw memory services.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
