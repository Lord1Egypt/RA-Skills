## Description:

Local semantic memory with vector search and Transformers.js. Store, search, and recall conversation context using embeddings (fully local, no API keys).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuiho-kai](https://clawhub.ai/user/zuiho-kai)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to give agents local long-term semantic memory for storing, searching, forgetting, and automatically recalling conversation context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memories may be saved as plaintext under the configured storage path.

Mitigation: Use the skill only where local plaintext memory is acceptable, set persistToDisk to false when durable storage is not needed, and review the storage path before enabling persistence.

Risk: Recalled memories may be inserted into future agent prompts.

Mitigation: Disable autoRecall when prior conversation memory should not influence future prompts, and periodically review or delete stored memories.

Risk: Conversation content may be captured automatically, including PII if allowPIICapture is enabled.

Mitigation: Keep autoCapture and allowPIICapture disabled unless explicit retention is intended, especially in shared, sensitive, or regulated environments.

Risk: Configured Qdrant storage can send memory content to an external server.

Mitigation: Use only trusted Qdrant servers and validate qdrantUrl before deployment.

Risk: Unvalidated collectionName or storagePath values can place retained memories in an unexpected location.

Mitigation: Validate collectionName and storagePath values before use and prefer an isolated storage directory.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zuiho-kai/skills/openclaw-semantic-memory)
- [Project homepage](https://github.com/zuiho-kai/openclaw-semantic-memory)
- [Issue tracker](https://github.com/zuiho-kai/openclaw-semantic-memory/issues)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool responses and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registers memory_store, memory_search, and memory_forget tools; may prepend recalled memories to agent context when autoRecall is enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
