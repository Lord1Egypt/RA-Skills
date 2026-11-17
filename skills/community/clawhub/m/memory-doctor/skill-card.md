## Description:

memory-doctor checks and tidies existing LLM agent memory stores by reporting health issues and applying deterministic index reconciliation for supported formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperkwok](https://clawhub.ai/user/casperkwok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to inspect existing Claude Code auto-memory or mneme stores for index drift, stale entries, dead links, duplicate candidates, oversized memories, and freshness. For auto-memory stores, they can preview or apply deterministic MEMORY.md index reconciliation when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory directories containing symlinks may allow reads or writes outside the selected directory.

Mitigation: Use only memory directories you control, avoid directories containing symlinks, and inspect the lint plan before running --fix.

Risk: Undo should not be treated as a complete rollback for all filesystem effects.

Mitigation: Keep independent backups before file-mutating commands and treat undo as a local best-effort restoration path.

Risk: --fix and undo mutate local memory files.

Mitigation: Run report and lint without --fix first, then apply changes only after reviewing the proposed index reconciliation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/casperkwok/skills/memory-doctor)
- [ClawHub publisher profile](https://clawhub.ai/user/casperkwok)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style CLI health report with command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only reporting is available; lint --fix and undo are local file-mutating commands.]

## Skill Version(s):

0.1.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
