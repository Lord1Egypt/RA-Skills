## Description:

用户与模型间的任何交互行为都会触发此技能；提供Context Engineering五大核心能力（选择、压缩、检索、状态、记忆）及认知模型层支持；作为元技能强制常驻运行.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwifruit13](https://clawhub.ai/user/kiwifruit13)

### License/Terms of Use:

GPL-3.0

## Use Case:

Developers and agent builders use this skill to add an always-on memory and context engineering layer that can select, compress, retrieve, track state, and preserve conversation-derived context across interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to run on every interaction and may store conversation-derived data.

Mitigation: Deploy only with explicit user consent for memory storage, clear retention and deletion controls, and a visible path to withdraw consent.

Risk: Persistent memory or Redis-backed storage can expose sensitive conversation context if storage is not hardened.

Mitigation: Use isolated credential storage, encryption, Redis authentication, TLS, and least-privilege access controls before enabling persistence.

Risk: The release has conflicting license evidence between server metadata and artifact declarations.

Mitigation: Confirm the authoritative license before publication or deployment and update release metadata or source documentation so they match.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kiwifruit13/skills/memory-and-context-engineering)
- [Architecture Overview](references/architecture_overview.md)
- [Architecture Execution Model](references/architecture_execution_model.md)
- [Dual Track Architecture Overview](references/dual_track_architecture_overview.md)
- [Usage Guide](references/usage_guide.md)
- [Privacy Guide](references/privacy_guide.md)
- [API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to configure persistent file or Redis-backed memory, consent checks, context reconstruction, compression, retrieval, and monitoring.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
