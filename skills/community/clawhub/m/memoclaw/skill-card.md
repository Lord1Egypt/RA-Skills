## Description:

Memory-as-a-Service for AI agents that stores and recalls memories with semantic vector search using wallet-based identity and x402 micropayments after the free tier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anajuliabit](https://clawhub.ai/user/anajuliabit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use MemoClaw to give AI agents persistent, searchable memory across sessions, including storing user preferences, project decisions, and session summaries, then retrieving relevant context for future prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected memories, queries, files, or transcripts may be sent to a third-party remote memory service under a wallet identity.

Mitigation: Use a dedicated low-value wallet, confirm MEMOCLAW_URL before use, and do not store secrets or sensitive personal or regulated data.

Risk: CLI operations can mutate or delete remote memories and may incur x402 charges after the free tier.

Mitigation: Require explicit approval before paid operations, transcript ingest, imports, exports, purge/delete, or commands using --force or --yes; use snapshots and dry runs where available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anajuliabit/skills/memoclaw)
- [MemoClaw Documentation](https://docs.memoclaw.com)
- [MemoClaw Website](https://memoclaw.com)
- [API Reference](api-reference.md)
- [Usage Examples](examples.md)
- [Full Agent Instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to call the MemoClaw CLI or HTTPS API; context output can be plain text or structured JSON depending on command options.]

## Skill Version(s):

1.23.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
