## Description:

Cloud-persistent memory for AI agents. Stateless plugins + TiDB Serverless = cross-session recall, multi-agent sharing, and hybrid vector + keyword search. Works with OpenClaw, Claude Code, and OpenCode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiffang](https://clawhub.ai/user/qiffang)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to give OpenClaw, Claude Code, OpenCode, and HTTP-based agents persistent cross-session memory backed by TiDB Cloud Serverless. It supports personal memory storage, hybrid vector and keyword search, multi-agent sharing, and CRDT-aware updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent memories, searches, and metadata may be stored outside the local session in TiDB Cloud or a self-hosted server.

Mitigation: Use the skill only for data approved for external storage, and review retention, sharing, and access controls before storing sensitive or regulated information.

Risk: Database credentials and optional embedding API keys may grant access to memory data or related services.

Mitigation: Use dedicated least-privilege credentials, avoid storing secrets in memory content, and prefer pinned or verified package versions during installation.

Risk: Shared multi-agent memory can expose one agent's stored context to another agent configured for the same memory space.

Mitigation: Separate personal, team, and sensitive workflows with distinct memory spaces, tokens, or database accounts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qiffang/skills/mnemo-memory)
- [mnemos GitHub Repository](https://github.com/qiffang/mnemos)
- [Design Doc](https://github.com/qiffang/mnemos/blob/main/docs/DESIGN.md)
- [CRDT Memory Proposal](https://github.com/qiffang/mnemos/blob/main/claude-notes/crdt-memory-proposal.md)
- [TiDB Cloud Serverless](https://tidbcloud.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce setup commands, plugin configuration, memory tool usage guidance, and integration notes for cloud-backed memory.]

## Skill Version(s):

0.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
