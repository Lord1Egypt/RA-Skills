## Description:

Local semantic memory with Qdrant and Transformers.js. Store, search, and recall conversation context using vector embeddings (fully local, no API keys).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuiho-kai](https://clawhub.ai/user/zuiho-kai)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to give agents local semantic memory for storing, searching, recalling, and forgetting conversation context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored conversation-derived memories can persist on disk by default and be injected into later sessions.

Mitigation: Use the skill only in personal or trusted environments, disable persistToDisk or autoRecall for sensitive work, and review stored memories regularly.

Risk: PII may be stored if automatic capture and PII capture are explicitly enabled.

Mitigation: Keep autoCapture and allowPIICapture disabled unless needed, and enable PII capture only after confirming the privacy impact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuiho-kai/skills/openclaw-memory-qdrant)
- [Repository homepage](https://github.com/zuiho-kai/openclaw-memory-qdrant)
- [Repository README](https://github.com/zuiho-kai/openclaw-memory-qdrant#readme)
- [Repository issues](https://github.com/zuiho-kai/openclaw-memory-qdrant/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing guidance for memory storage, search, recall, deletion, and plugin configuration.]

## Skill Version(s):

1.0.15 (source: frontmatter, package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
