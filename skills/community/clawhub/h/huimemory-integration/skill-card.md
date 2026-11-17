## Description:

Guides developers through integrating HuiMemory as a local semantic conversation memory system with retrieval, time filtering, context expansion, and LLM tool schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neko1688](https://clawhub.ai/user/neko1688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add long-term local conversation memory, semantic recall, time-based filtering, and LLM recall tools to AI applications. It supports both non-intrusive augmentation of an existing memory stack and fuller memory-core integration for new applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent conversation memory can expose sensitive user data if conversations are indexed without consent.

Mitigation: Index only opted-in conversations, redact sensitive content before storage, and document retention and deletion behavior for users.

Risk: Retrieved conversation snippets may be sent to a remote LLM provider during memory-augmented chat.

Mitigation: Filter or summarize retrieved memories before model calls and avoid sending raw private conversations unless the user has approved that data flow.

Risk: Raw retrieved memories can contain prompt-injection content that may influence privileged instructions.

Mitigation: Treat retrieved memory as untrusted user-context data and keep it out of system or developer instructions.

Risk: The guide depends on external repositories, Python dependencies, and model artifacts.

Mitigation: Use a disposable virtual environment or container, pin dependencies and repositories to audited versions, and verify downloaded model artifacts.

## Reference(s):

- [HuiMemory Architecture](references/architecture.md)
- [HuiMemory API Reference](references/api-reference.md)
- [LLM Integration Guide](references/llm-integration.md)
- [HuiMemory repository](https://gitee.com/HuiMengAI/hui-memory.git)
- [BGE base Chinese v1.5 model mirror](https://gitcode.com/hf_mirrors/BAAI/bge-base-zh-v1.5.git)
- [BGE small Chinese v1.5 model mirror](https://gitcode.com/hf_mirrors/BAAI/bge-small-zh-v1.5.git)
- [BGE-M3 model mirror](https://gitcode.com/hf_mirrors/BAAI/bge-m3.git)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline JSON, YAML, Python, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces integration instructions, system prompt templates, tool schemas, configuration examples, and quickstart code for agent implementation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
