## Description:

Local semantic memory with Qdrant and Transformers.js. Store, search, and recall conversation context using vector embeddings (fully local, no API keys).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuiho-kai](https://clawhub.ai/user/zuiho-kai)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to give an agent local semantic memory, including storing, searching, recalling, and deleting remembered conversation context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual installation documentation points to a different GitHub owner than the server-resolved and canonical zuiho-kai source.

Mitigation: Install through ClawHub or the canonical zuiho-kai repository only, and avoid the inconsistent manual clone URL until corrected.

Risk: Stored memories and auto-captured conversation content can influence future prompts and may include sensitive information.

Mitigation: Keep autoCapture disabled unless intentional, review stored memories regularly, and delete memories that should not persist.

Risk: Qdrant mode sends stored memory data to the configured Qdrant server.

Mitigation: Use only trusted Qdrant servers, preferably a local instance or a dedicated service account for sensitive environments.

Risk: The skill downloads dependencies from npm and an embedding model from Hugging Face during installation or first run.

Mitigation: Use reproducible installation with locked dependencies and review or update dependencies before use in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zuiho-kai/skills/memory-qdrant)
- [GitHub Repository](https://github.com/zuiho-kai/openclaw-memory-qdrant)
- [GitHub README](https://github.com/zuiho-kai/openclaw-memory-qdrant#readme)
- [GitHub Issues](https://github.com/zuiho-kai/openclaw-memory-qdrant/issues)
- [Qdrant](https://qdrant.tech/)
- [Transformers.js](https://huggingface.co/docs/transformers.js)
- [OpenClaw](https://openclaw.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [OpenClaw tool responses as text containing JSON status payloads, plus Markdown guidance with JavaScript, JSON, and shell examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exposes memory_store, memory_search, and memory_forget tools; auto-recall can inject relevant memories into prompt context when enabled.]

## Skill Version(s):

1.0.10 (source: frontmatter, package.json, CHANGELOG, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
