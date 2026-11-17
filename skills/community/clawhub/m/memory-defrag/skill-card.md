## Description:

Defragment and reorganize agent memory files: split bloated files, merge duplicates, remove stale information, and restructure the memory hierarchy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phernandez](https://clawhub.ai/user/phernandez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit, reorganize, split, merge, and prune local agent memory files while preserving useful context and audit trails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pruning or scheduled defragmentation could remove useful memory or task context.

Mitigation: Review proposed deletions before applying them, preserve raw daily notes, and keep uncertain entries marked for review instead of deleting them.

Risk: Merging or restructuring memory files can accidentally lose context or break cross-references.

Mitigation: Compare before and after states, update cross-references, and log the files reviewed, split, merged, pruned, and changed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phernandez/skills/memory-defrag)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files, Shell commands]

**Output Format:** [Markdown guidance with optional file edits, checklists, logs, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose splitting, merging, pruning, renaming, and logging changes to memory files.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
