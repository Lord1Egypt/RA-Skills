## Description:

Local long-term memory setup guidance for OpenClaw using mem0, ChromaDB, DeepSeek for LLM-based fact extraction, and DashScope for embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dream-star-end](https://clawhub.ai/user/dream-star-end)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install and configure a local mem0 memory server, connect it to OpenClaw, and optionally import existing workspace memory files into a shared semantic memory pool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup asks users to run external repository code that is not pinned to a reviewed commit.

Mitigation: Pin the repository to a reviewed commit before installation and review the setup scripts before execution.

Risk: The memory pool is shared across agents and can persist sensitive or operational details across sessions.

Mitigation: Use the shared memory pool only when that data boundary is acceptable, and review or redact workspace files before import.

Risk: Memory snippets are sent to third-party DeepSeek and DashScope APIs for extraction and embedding.

Mitigation: Avoid importing secrets or sensitive content, and store API keys using secure user-level secret handling.

Risk: Persistent service configuration can expand exposure if the endpoint or service scope is misconfigured.

Mitigation: Keep the endpoint bound to loopback, avoid system-wide auto-start where possible, and prefer user-level service configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dream-star-end/skills/mem0-local-memory)
- [Project repository referenced by the skill](https://github.com/dream-star-end/openclaw-plugin-mem0-local)
- [DeepSeek API platform](https://platform.deepseek.com/)
- [DashScope API platform](https://dashscope.aliyuncs.com/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, JSON, and INI configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, verification, troubleshooting, and import guidance for a local memory service.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
