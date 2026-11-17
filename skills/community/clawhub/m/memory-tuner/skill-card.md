## Description:

按读取频率追踪并优化 MEMORY.md 长期记忆：埋点、冷热统计、降级/上移/清理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[smliences](https://clawhub.ai/user/smliences)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to review long-term MEMORY.md entries by read frequency, identify hot, cold, frozen, and untracked memories, and plan memory archiving or cleanup with user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently track which memory entries are used.

Mitigation: Install it only when local memory-use tracking is intended, and review generated tracking files as part of memory maintenance.

Risk: Running maintenance against the wrong workspace could produce misleading reports or mark the wrong MEMORY.md entries.

Mitigation: Confirm OPENCLAW_WORKSPACE points to the intended workspace before running reports or using --mark.

Risk: Archive or cleanup actions can reorganize or remove long-term memory content.

Mitigation: Review the dry-run report and require explicit approval before archiving or cleanup actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smliences/skills/memory-tuner)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report, optional JSON report, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and may use OPENCLAW_WORKSPACE to select the target workspace.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
