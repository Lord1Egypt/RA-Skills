## Description:

Defragments and optimizes agent memory files by identifying duplicate entries, stale content, tiering issues, and formatting problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klemenska](https://clawhub.ai/user/klemenska)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect agent memory files, generate cleanup plans, create backups, and verify basic memory file integrity during maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The execute path can report archive or compact actions even though the scanned implementation only creates backups and prints status.

Mitigation: Treat --execute as an analyzer and backup path unless the implementation is fixed; review the plan and manually verify file changes before relying on cleanup results.

Risk: Backup copies may contain sensitive agent memory and identity state.

Mitigation: Restrict access to .defrag_backup contents and remove backup copies after the recovery window when they are no longer needed.

## Reference(s):

- [Memory Defragmentation Rules](references/rules.md)
- [ClawHub skill page](https://clawhub.ai/klemenska/skills/memory-defragmenter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown plan plus terminal text reports and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create defragment-plan.md and .defrag_backup copies when the bundled scripts are run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
