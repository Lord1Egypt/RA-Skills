## Description:

Memento gives OpenClaw agents local persistent memory by capturing conversations, extracting structured facts via an LLM, and auto-recalling relevant knowledge before each turn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[braibaud](https://clawhub.ai/user/braibaud)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users, developers, and engineers use Memento to give agents persistent local memory, structured fact extraction, and pre-turn recall across conversations. It is suited for users who want long-term assistant continuity while keeping captured data on local storage unless optional LLM-backed extraction or query planning is enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic extraction or query planning can send conversation content to configured LLM providers.

Mitigation: Keep autoExtract and autoQueryPlanning disabled for sensitive conversations, or configure a local Ollama model for extraction and planning.

Risk: Long-term memory stores complete chats and extracted facts on local disk.

Mitigation: Restrict filesystem permissions on the data directory and review or remove the SQLite database and JSONL backups when they are no longer needed.

Risk: Cross-agent recall can expose private memories according to the security summary.

Mitigation: Disable crossAgentRecall until the private-fact graph traversal issue is fixed and visibility behavior has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/braibaud/skills/memento)
- [Publisher profile](https://clawhub.ai/user/braibaud)
- [README](README.md)
- [Project design document](docs/PROJECT.md)
- [Declared project repository](https://github.com/braibaud/Memento)
- [BGE-M3 model card](https://huggingface.co/BAAI/bge-m3)
- [BGE-M3 GGUF download reference](https://huggingface.co/gpustack/bge-m3-GGUF/resolve/main/bge-m3-Q8_0.gguf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, shell command examples, and recalled memory context injected into agent prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores conversation segments, extracted facts, embeddings, and recall metadata in local SQLite and JSONL files.]

## Skill Version(s):

0.6.0 (source: frontmatter, package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
