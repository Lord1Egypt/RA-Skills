## Description:

Memory Compactor organizes and compresses long-term memory by summarizing redundant content and clearing outdated information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soroyue](https://clawhub.ai/user/soroyue)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers use this skill to maintain persistent memory files by summarizing older entries, retaining key decisions and lessons, and removing stale temporary information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic memory summarization or cleanup can rewrite or remove persistent memory without clear preview, confirmation, or rollback.

Mitigation: Require a preview, explicit user confirmation, and recoverable backups before applying memory changes.

Risk: Important decisions, preferences, or lessons may be lost if the compaction rules classify them as outdated or redundant.

Mitigation: Keep long-term identity, goals, rules, decisions, and lessons in protected sections that are reviewed manually before deletion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soroyue/skills/memory-compactor)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown memory summaries and file update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize, deduplicate, or remove memory content according to documented retention levels.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
