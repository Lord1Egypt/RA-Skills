## Description:

Memory health monitoring, integrity checks, and 3-layer memory architecture for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to monitor markdown-based agent memory, detect oversized, stale, duplicate, or orphaned files, and plan session-to-permanent memory promotion or recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact advises preserving credentials or keys in permanent, git-tracked memory.

Mitigation: Do not copy credentials into markdown memory, archives, embeddings, or git history; use a dedicated secrets manager and redact secrets from memory files.

Risk: Promotion, cleanup, deletion, recovery, or migration steps can alter or remove memory content.

Mitigation: Use read-only checks by default, require explicit user review before changes, and create backups before cleanup or recovery operations.

## Reference(s):

- [Memory Guardian release page](https://clawhub.ai/dodge1218/skills/memory-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and diagnostic text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a Python health-check script that reports file size, staleness, duplicate content, index consistency, and orphaned memory files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
