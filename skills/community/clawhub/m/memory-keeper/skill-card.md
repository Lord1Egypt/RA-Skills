## Description:

Copy and snapshot all important agent context (MEMORY.md, memory/*.md, AGENTS.md, SOUL.md, etc.) into a dedicated archive directory or repo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crimsondevil333333](https://clawhub.ai/user/crimsondevil333333)

### License/Terms of Use:


## Use Case:

External users and developers use Memory Keeper to create durable snapshots of OpenClaw agent memory and context files before maintenance, risky changes, recovery, or migration. It can keep archives local or prepare them for a user-controlled git repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory archives may contain sensitive agent context, private notes, configuration, or secrets.

Mitigation: Review and redact memory files before archiving or sharing, and prefer local-only archives unless the destination is trusted.

Risk: The optional push workflow can send sensitive archive contents to a remote git repository.

Mitigation: Use --push only with a private repository you own, verify the remote URL and branch first, and avoid using the documented example remote for personal memories.

Risk: Embedding tokens in git URLs or shell commands can expose credentials.

Mitigation: Use SSH keys or a credential helper instead of placing tokens directly in commands or remote URLs.

Risk: Broad --allow-extra patterns can copy files beyond the intended memory set.

Mitigation: Keep extra patterns narrow and inspect the matched files before syncing.

## Reference(s):

- [Memory Keeper usage reference](references/usage.md)
- [ClawHub skill page](https://clawhub.ai/crimsondevil333333/skills/memory-keeper)
- [Publisher profile](https://clawhub.ai/user/crimsondevil333333)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local archive files and optional git commits or pushes when the generated commands are executed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
