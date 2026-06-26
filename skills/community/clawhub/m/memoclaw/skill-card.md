## Description: <br>
Memory-as-a-Service for AI agents that stores and recalls memories with semantic vector search using wallet-based identity and x402 micropayments after the free tier. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anajuliabit](https://clawhub.ai/user/anajuliabit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use MemoClaw to give agents persistent semantic memory across sessions, including storing preferences, decisions, project context, and session summaries. It is most useful when memory should survive context resets or be shared through namespaces instead of kept in local scratch files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload persistent personal, project, or conversation data to a remote memory service. <br>
Mitigation: Do not store secrets or sensitive personal data, recall before storing to avoid unnecessary duplication, and periodically review, export, or delete memories that should not persist. <br>
Risk: Wallet-based authentication and paid x402 calls use a private key and can incur charges after the free tier. <br>
Mitigation: Use a dedicated low-balance wallet, verify the MemoClaw endpoint before use, and require manual approval for paid commands and for ingest, migrate, export, purge, force, and yes operations. <br>
Risk: Bulk ingest, migration, consolidation, and destructive commands can process or remove many memories at once. <br>
Mitigation: Preview or scope bulk operations where possible, create a snapshot before destructive changes, and require explicit user approval before purge, force, or yes flags are used. <br>


## Reference(s): <br>
- [MemoClaw Skill on ClawHub](https://clawhub.ai/anajuliabit/memoclaw) <br>
- [MemoClaw Documentation](https://docs.memoclaw.com) <br>
- [MemoClaw Website](https://memoclaw.com) <br>
- [README.md](README.md) <br>
- [examples.md](examples.md) <br>
- [api-reference.md](api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON or markdown outputs from MemoClaw CLI/API commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can store, recall, update, export, import, migrate, and delete remote memories; paid operations may require USDC on Base after the free tier.] <br>

## Skill Version(s): <br>
1.23.5 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
