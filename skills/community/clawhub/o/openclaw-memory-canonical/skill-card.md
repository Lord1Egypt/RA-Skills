## Description:

Lightweight file-based memory system for single-user AI agents using markdown memory tiers, working buffers, health checks, archival, recovery, and lesson-promotion workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain persistent local memory for a single-user AI agent, including session context loading, buffer rotation, recovery, archival, health validation, and reusable lesson capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad activation triggers for persistent local memory.

Mitigation: Install it only in workspaces where persistent agent memory is intended, and review activation language before deployment.

Risk: File-maintenance scripts can overwrite stored records in edge cases.

Mitigation: Review the shell scripts before relying on important records, prefer non-shared writable memory directories, and patch archival or temporary-file handling if stronger no-clobber guarantees are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ciklopentan/skills/openclaw-memory-canonical)
- [Upgrade & Runtime Re-Sync Contract](artifact/UPGRADE.md)
- [Verification Evidence](artifact/references/verification-evidence.md)
- [Reference Test Log](artifact/references/reference-test-log.md)
- [Decision Rationale](artifact/references/design-rationale.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file path conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct local writes to workspace memory files and maintenance scripts.]

## Skill Version(s):

4.6.14 (source: server evidence, _meta.json, CHANGELOG, and SKILL.md heading; released 2026-04-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
